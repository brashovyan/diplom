from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from .models import *
from userapp.serializers import UserSerializer


# Посуда
class CookwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookware
        fields = "__all__"


# Ингредиенты
class IngregientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'title', 'price']


# Отзывы
class ReviewSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Review
        fields = "__all__"


# отображение списка блюд
class DishListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Dish
        fields = ['id', 'title', 'description', 'calories', 'time', 'likes', 'dislikes', 'creator', 'mainphoto']


# Детальное отображение блюда
class DishDetailSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True, many=False)
    cookware = CookwareSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Dish
        fields = "__all__"


# Создание блюда
class DishCreateSerializer(serializers.ModelSerializer):
    # это, чтобы автоматически подтягивался юзер
    creator = serializers.ReadOnlyField(source='creator.id')


    class Meta:
        model = Dish
        fields = "__all__"

