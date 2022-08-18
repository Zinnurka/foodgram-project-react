from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.core import validators

from .validators import validate_cooking_time

User = get_user_model()


class Tags(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(max_length=200, verbose_name='Цветовой HEX-код')
    slug = models.SlugField(verbose_name='Slug', unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(max_length=200, verbose_name='Мера')


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[validate_cooking_time]
    )
    is_favorited = models.BooleanField(
        verbose_name='Показывать только рецепты,находящиеся в '
                     'списке избранного.')
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Показывать только рецепты, находящиеся в списке покупок')
    tags = models.ManyToManyField(Tags, through='RecipeTags')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингридиент',
        related_name='recipes',
    )
    image = models.ImageField(upload_to=f'recipe/{datetime.now().date()}/',
                              blank=True)


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Минимум 1'),),
        verbose_name='Количество',
    )


class RecipeTags(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
