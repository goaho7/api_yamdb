from django_filters import rest_framework as f
from reviews.models import Title


class FilterByTitle(f.FilterSet):
    """Фильтр полей для модели Title."""

    category = f.CharFilter(field_name='category__slug')
    genre = f.CharFilter(field_name='genre__slug')
    name = f.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
