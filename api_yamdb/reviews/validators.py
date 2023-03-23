import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка года выпуска произведения."""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Год выпуска произведения не должен превышать текущий год'
        )
    return value


def username_validator(value):
    """Проверка поля username"""

    pattern = r'[\w.@+-]+'
    error_chars = ', '.join(set(re.sub(pattern, '', value)))
    error_message = f'Строка содержит запрещенные символы: {error_chars}'
    if error_chars:
        raise ValidationError(error_message)

    if value.lower() == 'me':
        raise ValidationError(
            f'Нельзя использовать {value} как имя пользователя'
        )

    return value
