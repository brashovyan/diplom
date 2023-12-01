from django.shortcuts import render, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from .serializers import *
from rest_framework import generics, viewsets
from django.contrib.auth import get_user_model
User = get_user_model()
from .permissions import *
from .models import *
from rest_framework.response import Response


# вообще любой может получить всю посуду
class CookwareView(generics.ListAPIView):
    permission_classes = []
    queryset = Cookware.objects.all()
    serializer_class = CookwareSerializer


# вообще любой может получить конкретную посуду по айди
class CookwareDetailView(generics.RetrieveAPIView):
    permission_classes = []
    queryset = Cookware.objects.all()
    serializer_class = CookwareSerializer


# Админ имеет полный доступ к посуде
class CookwareViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Cookware.objects.all()
    serializer_class = CookwareSerializer


# вообще любой может получить все ингредиенты
class IngredientView(generics.ListAPIView):
    permission_classes = []
    queryset = Ingredient.objects.all()
    serializer_class = IngregientSerializer


# вообще любой может получить конкретный ингредиент по айди
class IngredientDetailView(generics.RetrieveAPIView):
    permission_classes = []
    queryset = Ingredient.objects.all()
    serializer_class = IngregientSerializer


# Любой зареганый юзер может добавить ингредиент
class IngredientCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ingredient.objects.all()
    serializer_class = IngregientSerializer


# Админ и модератор имеет полный доступ к ингредиентам
class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser|IsModerator]
    queryset = Cookware.objects.all()
    serializer_class = CookwareSerializer


# создавать блюда могут любые зареганные юзеры
class DishCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DishCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['creator'] = self.request.user
        serializer.save()
        dish = Dish.objects.get(pk=serializer.data["id"])

        # после того, как создали блюдо, добавляем ингредиенты
        for ingredient_dict in request.data["ingredients"]:
            for ingredient, count in ingredient_dict.items():
                try:
                    # пытаюсь найти ингредиент по названиям
                    ing = Ingredient.objects.filter(other_names__contains = ingredient.strip().lower())
                    if ing:
                        # если нашёл, то просто добавляю в блюдо
                        dishingredient = DishIngredients(dish=dish, ingredient=ing[0], count=count)
                        dishingredient.save()
                    else:
                        # если не нашел, то сначала я создаю этот ингредиент
                        new_ingredient = Ingredient(title=ingredient, other_names=ingredient.strip().lower())
                        new_ingredient.save()

                        # а потом добавляю в блюдо
                        dishingredient = DishIngredients(dish=dish, ingredient=new_ingredient, count=count)
                        dishingredient.save()
                except:
                    pass # на всякий случай, чтобы краша не было

        # json, который я жду (лайки, дизлайки, отзывы, логично, пустые. Modercheck по дефолту False)
        """
            {
                "title": "Название блюда",
                "description": "Описание блюда",
                "proteins": 100,
                "fats": 100,
                "carbohydrates": 100,
                "calories": 500,
                "breakfast": true,
                "lunch": true,
                "dinner": true,
                "usualdiet": true,
                "weightloss": true,
                "weightgain": true,
                "recipe": "сам рецепт, просто много текста",
                "time": "5 минут",
                "cookware": [1, 2],
                "mainphoto": photo,
                "photo1": photo,
                "photo2": photo,
                и так далее фотки (они необязательны)
                "ingredients": [{"молоко": "200 мл"}, {"яйца": "5 шт"}, {"картофель": "100 гр"}]
            }
        """
        return Response({'message': serializer.data})


# На одной странице будет 25 блюд
class DishPagination(PageNumberPagination):
    page_size = 25
    page_query_param = 'page_size'
    max_page_size = 100


# любой может получить список всех блюд (с пагинацией)
class DishListView(generics.ListAPIView):
    permission_classes = []
    pagination_class = DishPagination
    queryset = Dish.objects.all()
    serializer_class = DishListSerializer


# любой может получить конкретное блюдо по айди
class DishDetailView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            dish = get_object_or_404(Dish, pk=pk)

            # заполняю список ингредиентов
            ingredients = DishIngredients.objects.filter(dish=dish)
            ingredients_list = []
            full_price = 0
            for ingredient in ingredients:
                ingredients_list.append({"id": ingredient.ingredient.id, "title": ingredient.ingredient.title,
                                         "price": ingredient.ingredient.price, "count": ingredient.count})
                full_price += ingredient.ingredient.price

            return Response({'dish': DishDetailSerializer(dish, many=False).data, "ingredients": ingredients_list, "full_price": full_price})







