from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_year, validate_regex


class Category(models.Model):
    """Категории произведений"""
    name = models.CharField('название категории', max_length=256)
    slug = models.SlugField(
        'ссылка категории',
        max_length=50,
        unique=True,
        validators=[validate_regex],
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
        validators=[validate_regex],
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


class Reviews(models.Model):
    """Отзывы"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

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
        Reviews, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
