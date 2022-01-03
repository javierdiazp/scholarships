from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import password_changed, validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import exceptions
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts import serializers
from mail import send_fake_mail

User = get_user_model()


def get_user_by_uidb64_or_404(uidb64):
    try:
        uid = int(force_str(urlsafe_base64_decode(uidb64)))
    except ValueError:
        raise Http404

    return get_object_or_404(User, pk=uid)


def validate_token(user, token):
    if not PasswordResetTokenGenerator().check_token(user, token):
        raise Http404


class ResetPasswordRequestToken(generics.GenericAPIView):
    serializer_class = serializers.EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({'detail': _('Email sent')})

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Send an e-mail to the user
        send_fake_mail(token, uid)

        return Response({'detail': _('Email sent')})


class ResetPasswordValidateToken(generics.GenericAPIView):
    serializer_class = serializers.UIDTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']

        user = get_user_by_uidb64_or_404(uidb64)
        validate_token(user, token)

        return Response({'detail': _('Token valid')})


class ResetPasswordConfirm(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        user = get_user_by_uidb64_or_404(uidb64)
        validate_token(user, token)

        try:
            validate_password(user=user, password=password)
        except exceptions.ValidationError as e:
            raise ValidationError(e.messages)

        user.set_password(password)
        user.save()

        password_changed(user=user, password=password)

        return Response({'detail': _('Password changed')})


class UpdatePasswordAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UpdatePasswordSerializer

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({"detail": _("Password changed")})


class CandidateCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.CandidateSerializer
