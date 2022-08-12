from rest_framework import serializers
from django.core.files.base import ContentFile
import base64
import uuid
import imghdr

ALLOWED_IMAGE_TYPES = (
    "jpeg",
    "jpg",
    "png"
)


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if not data:
            return None
        if isinstance(data, str):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except ValueError:
                raise serializers.ValidationError('Не получается '
                                                  'декодировать изображение')
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            if file_extension not in ALLOWED_IMAGE_TYPES:
                raise serializers.ValidationError('Данный тип изображений не '
                                                  'поддерживается')
            complete_file_name = "%s.%s" % (file_name, file_extension,)
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension
