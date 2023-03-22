from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import FilterByTitle
from api.mixins import CreateListDestroyViewSet
from api.permissions import (IsAdmin, IsAdministratorOrReadOnly,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, MeSerializer, ReviewSerializer,
                             SignupSerializer, TitleCreateUpdateSerializer,
                             TitleSerializer, TokenSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """Отзывы"""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии"""

    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyViewSet):
    """Категории произведений"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdministratorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Жанры произведений"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения"""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all().order_by('name')
    permission_classes = (IsAdministratorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterByTitle

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateUpdateSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями"""

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Метод редактирования при запросе на users/me/"""

        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = MeSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupView(APIView):
    """Создание пользователя и отправка кода подтверждения."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            **serializer.validated_data,
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения.',
            f'Код для регистрации: {confirmation_code}',
            settings.EMAIL,
            [f'{user.email}'],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """Получение JWT токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = 'Неверный код подтверждения'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)
