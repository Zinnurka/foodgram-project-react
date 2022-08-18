from django.contrib import admin
from .models import Recipe, Tags, Ingredient


admin.site.register(Recipe)
admin.site.register(Tags)
admin.site.register(Ingredient)
