import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from rooms.models import Room
from rooms.models.room import Message

User = get_user_model()


class AuthenticationError(Exception):
    pass


class RoomConsumer(WebsocketConsumer):
    AUTH_TOKEN_VALIDATION_ERROR_ON_CONNECT = 3001
    AUTH_TOKEN_VALIDATION_ERROR_ON_MSG = 3002

    room = room_uuid = room_group_name = user = None

    def connect(self):
        self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
        self.room_group_name = 'chat_%s' % self.room_uuid

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        try:
            self.authenticate()
        except AuthenticationError:
            self.close(self.AUTH_TOKEN_VALIDATION_ERROR_ON_CONNECT)
        else:
            self.accept()

    def authenticate(self):
        token = self.scope['cookies'].get('token')

        try:
            access_token = AccessToken(token)
        except TokenError:
            raise AuthenticationError

        user_id = access_token['user_id']

        try:
            self.user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationError

        try:
            self.room = Room.objects.get(Q(pk=user_id), Q(candidate=self.user) | Q(evaluator=self.user))
        except Room.DoesNotExist:
            raise AuthenticationError

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        if data['command'] == 'send_message':
            self.send_message(data)

        elif data['command'] == 'fetch_messages':
            pass

    def send_message(self, data):
        """ Send message to room group """
        Message.objects.create(room=self.room, author=self.user, content=data['message'])

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'receive_message',
                'message': data
            }
        )

    def receive_message(self, event):
        """ Receive message from room group """
        self.send(text_data=json.dumps({
            'message': event['message']
        }))

    # def fetch_messages(self, data):
    #     messages = self.get_last_messages(from_timestamp=data['timestamp'], limit=1000)
    #
    #     content = {
    #         'command': 'fetch_messages',
    #         'messages': [message.as_json() for message in messages]
    #     }
    #     self.send_message(content)
