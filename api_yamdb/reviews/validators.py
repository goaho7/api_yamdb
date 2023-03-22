from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка года выпуска произведения."""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Год выпуска произведения не должен превышать текущий год')
    return value
