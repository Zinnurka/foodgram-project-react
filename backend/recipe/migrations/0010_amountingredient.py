# Generated by Django 4.1 on 2022-08-15 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_recipe_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=20)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.ingredient', verbose_name='Ингредиент')),
            ],
        ),
    ]
