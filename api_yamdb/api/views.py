from rest_framework.views import APIView
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator

from api_yamdb.settings import EMAIL

User = get_user_model()


class SignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid()
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
            )
        except IntegrityError:
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        User.objects.filter(username=username).update(
            confirmation_code=confirmation_code
        )

        send_mail(
            'Код подтверждения.',
            f'Код для регистрации: {confirmation_code}',
            EMAIL,
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    pass
