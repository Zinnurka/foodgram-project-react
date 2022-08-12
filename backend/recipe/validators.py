import base64

from django.core.exceptions import ValidationError


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            'Значение должно быть положительным',
            params={'value': value},
        )


def validate_image(value):
    if not base64.b64decode(value):
        raise ValidationError(
            'Не получается',
            params={'value': value},
        )
