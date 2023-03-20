from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator


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
