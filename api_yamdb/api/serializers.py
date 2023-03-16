from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me' or '':
            raise serializers.ValidationError(
                'Нельзя использовать me в качестве имени пользователя.'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь username уже зарегистрирован.'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Такой email уже зарегистрирован.'
            )
        return value
