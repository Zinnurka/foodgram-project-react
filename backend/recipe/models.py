from django.db import models
from .validators import validate_cooking_time


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(verbose_name='Время приготовления (в минутах)',
                                       validators=[validate_cooking_time]
                                       )
