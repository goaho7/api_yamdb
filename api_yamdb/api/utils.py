from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.pagination import PageNumberPagination

from api.permissions import IsAdministratorOrReadOnly
from reviews.validators import username_validator


class GenreCategoryBaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    pagination_class = PageNumberPagination
    permission_classes = (IsAdministratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UsernameCharField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['max_length'] = kwargs.get(
            'max_length', settings.MAX_LENGTH_SLUG
        )
        self.validators.append(UnicodeUsernameValidator())
        self.validators.append(username_validator)
        super().__init__(**kwargs)
