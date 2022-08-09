from django.core.paginator import Paginator
from rest_framework import viewsets, permissions, status, filters
from rest_framework import viewsets
from recipe.models import Recipe
from .serializers import RecipeSerializer


class RecipeVeiwSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
