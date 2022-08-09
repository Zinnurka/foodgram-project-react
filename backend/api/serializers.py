from rest_framework import serializers, exceptions

from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = Recipe
        fields = '__all__'
