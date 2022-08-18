from rest_framework import viewsets
from recipe.models import Recipe, Tags
from .serializers import RecipeSerializer, TagSerializer
from rest_framework.parsers import JSONParser, MultiPartParser


class RecipeVeiwSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    parser_classes = (MultiPartParser, JSONParser)


class TagVeiwSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
