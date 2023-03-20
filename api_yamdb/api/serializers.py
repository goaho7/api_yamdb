import re
from django.utils import timezone

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title).exists():
            raise serializers.ValidationError(
                "Вы уже писали отзыв к этому произведению."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений"""

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений"""

    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений"""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), many=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        """Проверка года выпуска произведения."""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может превышать текущий год!'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя"""
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
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать me в качестве имени пользователя.'
            )
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'username некорректный.'
            )
        if len(value) > 150:
            raise serializers.ValidationError(
                'Длина email должна быть меньше 150 символов.'
            )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                'Длина email должна быть меньше 254 символов.'
            )
        return value

    def validate(self, data):
        username = User.objects.filter(username=data.get('username'))
        email = User.objects.filter(email=data.get('email'))
        if username and not email:
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if email and not username:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токена."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )
