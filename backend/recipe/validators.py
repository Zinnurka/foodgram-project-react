import base64

from django.core.exceptions import ValidationError


def validate_image(value):
    if not base64.b64decode(value):
        raise ValidationError(
            'Не получается',
            params={'value': value},
        )
