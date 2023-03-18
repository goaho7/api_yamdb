from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .validators import validate_year
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    """Категории произведений"""
    name = models.CharField('название категории', max_length=256)
    slug = models.SlugField(
        'ссылка категории',
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
        message='Содержит неизвестный символ')],
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений"""
    name = models.CharField('название категории', max_length=256)
    slug = models.SlugField(
        'ссылка категории',
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
        message='Содержит неизвестный символ')],
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения"""

    name = models.CharField('название произведения', max_length=256)
    year = models.PositiveSmallIntegerField('год создания произведения', validators=[validate_year])
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(Category, related_name='titles', on_delete=models.SET_NULL, null=True)
    description = models.CharField(
        'описание произведения',
        max_length=256,
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
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
