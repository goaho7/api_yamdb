from api.serializers import ReviewsSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Reviews


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.Reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
