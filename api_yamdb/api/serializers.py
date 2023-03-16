from reviews.models import Reviews, Category, Genre, Title
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


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
