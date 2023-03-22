import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone

validate_regex = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Содержит неизвестный символ'
)


def validate_year(value):
    """Проверка года выпуска произведения."""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Год выпуска произведения не должен превышать текущий год')
    return value


def username_validator(value):
    if value.lower() == 'me':
        raise ValidationError(
            f'Нельзя использовать {value} как имя пользователя'
        )
    elif len(value) > 150:
        raise ValidationError(
            'Имя пользователя не должно быть больше 150 символов'
        )
    elif not re.fullmatch(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'Имя пользователя содержит неверный символ'
        )
    return value
