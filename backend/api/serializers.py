import base64

from rest_framework import serializers
from recipe.models import Recipe, Tags, Ingredient
from .fields import Base64ImageField


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
    image = Base64ImageField(
        max_length=None, use_url=True, label='Картинка'
    )

    class Meta:
        ordering = ['-id']
        model = Recipe
        fields = '__all__'
