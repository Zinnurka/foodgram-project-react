from django.urls import include, path
from .views import RecipeVeiwSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('recipes', RecipeVeiwSet)
urlpatterns = [
    path('', include(router.urls)),
]
