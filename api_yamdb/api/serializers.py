from reviews.models import Reviews
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
