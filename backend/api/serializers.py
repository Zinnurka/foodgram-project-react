from rest_framework import serializers, exceptions
from django.core.files.base import ContentFile
from recipe.models import Recipe, Tags, Ingredient
import base64


class Base64ImageField(serializers.ImageField):
    def from_native(self, data):
        if data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super(Base64ImageField, self).from_native(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    image = Base64ImageField

    class Meta:
        ordering = ['-id']
        model = Recipe
        fields = '__all__'
