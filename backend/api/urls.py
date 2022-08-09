from django.urls import include, path
from rest_framework import routers
from .views import RecipeVeiwSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('recipe', RecipeVeiwSet)
urlpatterns = [
    path('', include(router.urls)),
]