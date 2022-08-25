from itertools import islice

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from recipe.models import Recipe, Tag, Ingredient, User, IngredientAmount
from .fields import Base64ImageField
from users.models import Follow
from users.serializers import CustomUserSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(
        many=True, required=True, source="ingredient_recipe"
    )

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objcts.all(),
                                              many=True)
    image = Base64ImageField(
        max_length=None, use_url=True, label='Картинка'
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()

    def validate_ingredients(self, data):
        ingredients = data['ingredients']
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Нужен хоть один ингридиент для рецепта'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError('Ингридиенты должны '
                                                  'быть уникальными')
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Убедитесь, что значение количества '
                                    'ингредиента больше 0')
                })
        return data

    def validate_cooking_time(self, cooking_time):
        if int(cooking_time) <= 1:
            raise serializers.ValidationError(
                'Убедитесь, что время готовки больше или равно 1')
        return cooking_time

    def validate_tags(self, tags):
        if UniqueValidator(queryset=Tag.objects.all()):
            return tags

    def create_ingredients(self, ingredients, recipe):
        batch_size = 100
        objs = (IngredientAmount(recipe=recipe, ingredient_id=ingredient.get(
                'id'), amount=ingredient.get('amount')) for ingredient in
                ingredients)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            IngredientAmount.objects.bulk_create(ingredients, batch_size)

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.pop("ingredients")
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)


class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True, label='Картинка'
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def validate(self, data):
        author = data['followed']
        user = data['follower']
        if user == author:
            raise serializers.ValidationError(
                'Вы не можете подписываться на самого себя и отписываться')
        if (Follow.objects.filter(author=author, user=user).exists()):
            raise serializers.ValidationError(
                'Вы уже подписаны на данного пользователя')
        return data
