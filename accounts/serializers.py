from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext as _
from rest_framework import serializers

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_('Email address'))


class UIDTokenSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(label=_('Password'))
    password_validation = serializers.CharField(label=_('Confirm password'))

    def validate_new_password(self, value):
        user = self.context['request'].user

        try:
            validate_password(password=value, user=user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate(self, attrs):
        password = attrs['password']
        password_validation = attrs['password_validation']

        if password != password_validation:
            raise serializers.ValidationError(_('Passwords must match'))

        return attrs


class ResetPasswordSerializer(PasswordSerializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()


class UpdatePasswordSerializer(PasswordSerializer):
    current_password = serializers.CharField(label=_('Current password'))

    def validate_current_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(_('Wrong password'))

        return value

    def update(self, instance, validated_data):
        user = instance
        user.set_password(validated_data['password'])
        user.save()

        return user


class CandidateSerializer(serializers.ModelSerializer, PasswordSerializer):
    class Meta:
        model = User

        fields = [
            'email',
            'password',
            'password_validation',
            'first_name',
            'last_name',
        ]

    def to_representation(self, instance):
        refresh_token, access_token = instance.get_jwt_tokens()
        return {'access': str(access_token), 'refresh': str(refresh_token)}

    def create(self, validated_data):
        validated_data.pop('password_validation')
        return User.objects.create_user(**validated_data, is_candidate=True)
