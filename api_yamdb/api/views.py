from api.filters import FilterByTitle
from api.mixins import CreateListDestroyViewSet
from api.permissions import (IsAdmin, IsAdministratorOrReadOnly,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleCreateUpdateSerializer,
                             TitleSerializer, TokenSerializer, UserSerializer)
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
from reviews.models import Category, Genre, Review, Title

from api_yamdb.settings import EMAIL

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """Отзывы"""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии"""

    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


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
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me_method(self, request):
        """Метод редактирования при запросе на users/me/"""

        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


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
        User.objects.filter(username=user.username).update(
            confirmation_code=confirmation_code
        )
        send_mail(
            'Код подтверждения.',
            f'Код для регистрации: {confirmation_code}',
            EMAIL,
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
