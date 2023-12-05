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


# Отображение отзыва
class ReviewListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Review
        fields = "__all__"


# Создание отзыва
class ReviewCreateSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ['date_review']


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
    reviews = ReviewListSerializer(read_only=True, many=True)

    class Meta:
        model = Dish
        fields = "__all__"


# Создание блюда (при создании никто не может указать лайки, дизлайки, отзывы, modercheck)
class DishCreateSerializer(serializers.ModelSerializer):
    # это, чтобы автоматически подтягивался юзер
    creator = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = Dish
        fields = ['title', 'description', 'proteins', "fats", "carbohydrates", "calories", "breakfast", "lunch",
                  "dinner",
                  "usualdiet", "weightloss", "weightgain", "recipe", "time", "mainphoto", "photo1", "photo2", "photo3",
                  "photo4", "photo5", "photo6", "photo7", "photo8", "photo9", "cookware", "creator", "id"]


# изменение блюда для обычного пользователя (он не может менять лайки, дизлайки, modercheck, отзывы)
class DishUpdateUsualUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['title', 'description', 'proteins', "fats", "carbohydrates", "calories", "breakfast", "lunch", "dinner",
                  "usualdiet", "weightloss", "weightgain", "recipe", "time", "mainphoto", "photo1", "photo2", "photo3",
                  "photo4", "photo5", "photo6", "photo7", "photo8", "photo9", "cookware"]


# изменение блюда для админа (он может делать че хочет)
class DishUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"


