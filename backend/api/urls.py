from django.urls import include, path
from .views import RecipeVeiwSet, TagVeiwSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('recipes', RecipeVeiwSet)
router.register('tags', TagVeiwSet)
urlpatterns = [
    path('', include(router.urls)),
]
