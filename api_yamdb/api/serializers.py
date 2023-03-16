
from django.contrib.auth import get_user_model

from reviews.models import Reviews, Category, Genre, Title
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


User = get_user_model()


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Reviews

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Reviews.objects.filter(
                author=author, title=title).exists():
            raise serializers.ValidationError(
                "Вы уже писали отзыв к этому произведению."
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений"""

    class Meta:
         fields = '__all__'
         model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений"""

    class Meta:
         fields = '__all__'
         model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений"""

    class Meta:
         fields = '__all__'
         model = Title


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


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


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токена."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )
