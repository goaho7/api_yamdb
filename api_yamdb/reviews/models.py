from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from reviews.validators import validate_year

from api_yamdb.settings import MAX_LENGTH_NAME, MAX_LENGTH_SLUG


class Category(models.Model):
    """Категории произведений"""
    name = models.CharField('название категории', max_length=MAX_LENGTH_NAME)
    slug = models.SlugField(
        'ссылка категории',
        max_length=MAX_LENGTH_SLUG,
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений"""
    name = models.CharField('название категории', max_length=MAX_LENGTH_NAME)
    slug = models.SlugField(
        'ссылка категории',
        max_length=MAX_LENGTH_SLUG,
        unique=True,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения"""

    name = models.CharField(
        'название произведения',
        max_length=MAX_LENGTH_NAME
    )
    year = models.PositiveSmallIntegerField(
        'год создания произведения',
        validators=[validate_year]
    )
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True)
    description = models.TextField(
        'описание произведения',
        blank=True,
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Кастомный пользователь"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ')
    )

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Содержит неизвестный символ'
        )],
        help_text=('Required. 150 characters or fewer.'
                   'Letters, digits and @/./+/-/_ only.')
    )

    bio = models.TextField(
        'Биография',
        blank=True
    )

    email = models.EmailField(
        verbose_name='Почта',
        unique=True,
        max_length=254
    )

    role = models.CharField(
        verbose_name='Роль',
        default='user',
        choices=ROLES,
        max_length=150
    )

    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        blank=True,
        max_length=150
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Review(models.Model):
    """Отзывы"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message='Рейтинг не может быть меньше 1'
            ),
            MaxValueValidator(
                10, message='Рейтинг не может быть больше 10'
            )
        ],
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Комментарии"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
