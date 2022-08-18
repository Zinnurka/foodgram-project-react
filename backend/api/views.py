from rest_framework import viewsets
from recipe.models import Recipe
from .serializers import RecipeSerializer
from rest_framework.parsers import JSONParser, MultiPartParser


class RecipeVeiwSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    parser_classes = (MultiPartParser, JSONParser)
