from django.urls import include, path
from api.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipeViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
