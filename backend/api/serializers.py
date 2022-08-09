from rest_framework import serializers, exceptions

from recipe.models import Recipe, Tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        ordering = ['-id']
        model = Recipe
        fields = '__all__'
