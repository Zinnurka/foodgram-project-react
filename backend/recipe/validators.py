from django.core.exceptions import ValidationError


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            'Значение должно быть положительным',
            params={'value': value},
        )
