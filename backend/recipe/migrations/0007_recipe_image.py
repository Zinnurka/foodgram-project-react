# Generated by Django 4.1 on 2022-08-10 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_recipeingredient_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipe/'),
        ),
    ]