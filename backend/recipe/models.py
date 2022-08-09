from django.db import models
from .validators import validate_cooking_time


class Tags(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(max_length=200, verbose_name='Цветовой HEX-код ')
    slug = models.SlugField(verbose_name='Slug', unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[validate_cooking_time]
    )
    is_favorited = models.BooleanField(
        verbose_name='Показывать только рецепты, ' \
                     'находящиеся в списке избранного.')
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Показывать только рецепты, находящиеся в списке покупок.')
    tags = models.ManyToManyField(Tags, through='RecipeTags')


class RecipeTags(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
