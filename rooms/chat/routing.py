from django.urls import path

from rooms.chat import consumer

websocket_urlpatterns = [
    path('ws/<str:country_code>/chat/<uuid:chat_uuid>/', consumer.ChatConsumer)
]
