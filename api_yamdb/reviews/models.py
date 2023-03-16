from django.db import models
from django.core.validators import RegexValidator


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
    year = models.PositiveSmallIntegerField('год создания произведения', max_length=4)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(Category, related_name='titles')
    description = models.CharField(
        'описание произведения',
        max_length=256,
        required=False,
    )

    def __str__(self):
        return self.name
