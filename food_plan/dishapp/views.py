from datetime import date
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
from .service import get_price


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
        for ingredient in request.data["ingredients"]:
            try:
                # Если у ингредиента нет айдишника
                if ingredient["id"] == "no":
                    # то я сначала создаю его
                    new_ingredient = Ingredient(title=ingredient["title"].strip().lower(), other_names=ingredient["title"].strip().lower())
                    new_ingredient.save()

                    # а потом добавляю в блюдо
                    dishingredient = DishIngredients(dish=dish, ingredient=new_ingredient, count=ingredient["count"])
                    dishingredient.save()

                # если у ингредиента есть айдишник
                else:
                    ing = get_object_or_404(Ingredient, pk=ingredient["id"])
                    # ing = Ingredient.objects.get(id=ingredient["id"])

                    # добавляю в блюдо
                    dishingredient = DishIngredients(dish=dish, ingredient=ing, count=ingredient["count"])
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
                "ingredients": [ { "id": "13", "title": "куриная грудка", "count": "300 гр" }, { "id": "4", "title": "картофель", "count": "5 шт" }, { "id": "no", "title": "лавровый лист", "count": "1 шт" } ]
            }
        """
        return Response({'message': serializer.data})


# обновление блюда (создатель, модер или админ)
class DishUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            dish = get_object_or_404(Dish, pk=pk)

            # проверяем что это создатель блюда (он не может изменять лайки, дизлайки, отзывы, modercheck)
            if request.user == dish.creator:
                serializer = DishUpdateUsualUserSerializer(data=request.data, instance=dish, partial=True, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                # когда обычный юзер изменяет блюдо, я снова ставлю modercheck = False. Мало ли чё он там наизменял
                dish.modercheck = False
                dish.in_algorithm = False
                dish.save()
                return Response({'title': serializer.data})

            # если это админ или модер (они могут менять всё)
            elif User.objects.filter(pk=request.user.id, groups__name='moderator').exists() or request.user.is_superuser:
                serializer = DishUpdateAdminSerializer(data=request.data, instance=dish, partial=True, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'title': serializer.data})

            else:
                return Response({"error": "Вы не можете изменить это блюдо"})


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
                                        "count": ingredient.count, "price": ingredient.ingredient.price,
                                         "last_update_price": ingredient.ingredient.last_update_price})
                full_price += ingredient.ingredient.price
            return Response({'dish': DishDetailSerializer(dish, many=False, context={"request": request}).data, "ingredients": ingredients_list, 'full_price': full_price})


# удаление блюда (создатель, админ или модер)
class DishDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            dish = get_object_or_404(Dish, pk=pk)
            if request.user == dish.creator or User.objects.filter(pk=request.user.id, groups__name='Moderator').exists() or request.user.is_superuser:
                dish.delete()
                return Response({"message": "Блюдо удалено!"})
            return Response({"error": "Вы не можете удалить это блюдо"})


# получение актуальной стоимости блюда (любой)
class DishActualPriceView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk", None)
            if pk:
                dish = get_object_or_404(Dish, pk=pk)
                ingredients = DishIngredients.objects.filter(dish=dish)
                full_price = 0
                result = []
                # проверяю все ингредиенты блюда
                for ingredient in ingredients:
                    # если нет даты последнего апдейта цены или она старше 14 дней
                    if not ingredient.ingredient.last_update_price or (date.today() - ingredient.ingredient.last_update_price).days >= 14:
                        # тогда обновляем цену и дату

                        # пытаюсь запарсить
                        try:
                            price = get_price(ingredient.ingredient.title)
                        # таймаут 20 секунд
                        except:
                            price = -1

                        # если получилось запарсить
                        if price != -1:
                            ingredient.ingredient.price = price
                            full_price += price
                            ingredient.ingredient.last_update_price = date.today()
                            ingredient.ingredient.save()
                            result.append({"id": ingredient.ingredient.id, 'title': ingredient.ingredient.title, "price": price, "last_update_price": ingredient.ingredient.last_update_price, "count": ingredient.count})

                        # если не получилось
                        else:
                            full_price += ingredient.ingredient.price
                            result.append({"id": ingredient.ingredient.id, 'title': ingredient.ingredient.title, "price": ingredient.ingredient.price, "last_update_price": ingredient.ingredient.last_update_price, "count": ingredient.count})

                    # если новая цена не нужна
                    else:
                        full_price += ingredient.ingredient.price
                        result.append({"id": ingredient.ingredient.id, 'title': ingredient.ingredient.title, "price": ingredient.ingredient.price, "last_update_price": ingredient.ingredient.last_update_price, "count": ingredient.count})
                return Response({"full_price": full_price, "ingredients": result})
        except:
            return Response({"error": "не удалось получить актуальные цены"})


# поставить лайк блюду (зареганые)
class DishLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            dish = get_object_or_404(Dish, pk=pk)
            dish.likes.add(request.user)
            dish.dislikes.remove(request.user)
            return Response({"message": f"Вы поставили лайк блюду {dish.title}"})


# поставить дизлайк блюду (зареганые)
class DishDislikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            dish = get_object_or_404(Dish, pk=pk)
            dish.dislikes.add(request.user)
            dish.likes.remove(request.user)
            return Response({"message": f"Вы поставили дизлайк блюду {dish.title}"})


# убрать лайк/дизлайк (очистить реакцию)
class DishClearLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            dish = get_object_or_404(Dish, pk=pk)
            dish.dislikes.remove(request.user)
            dish.likes.remove(request.user)
            return Response({"message": f"Вы удалили реакцию на {dish.title}"})


# создать комментарий может любой пользователь
class ReviewCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            dish = get_object_or_404(Dish, pk=pk)

            # создаю сам комментарий
            serializer = ReviewCreateSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['creator'] = self.request.user
            serializer.save()
            review = Review.objects.get(pk=serializer.data["id"])

            # добавляю его в блюдо
            dish.reviews.add(review)
            return Response({"message": f"Вы добавили комментарий к блюду {dish.title}"})


# изменение и удаление коментария (создатель, админ или модер)
class ReviewUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            review = get_object_or_404(Review, pk=pk)
            if request.user == review.creator or User.objects.filter(pk=request.user.id, groups__name='Moderator').exists() or request.user.is_superuser:
                serializer = ReviewCreateSerializer(data=request.data, instance=review, partial=True, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"message": f"Вы изменили комментарий"})
            return Response({"error": "Вы не можете редактировать этот комментарий"})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            review = get_object_or_404(Review, pk=pk)
            if request.user == review.creator or User.objects.filter(pk=request.user.id, groups__name='Moderator').exists() or request.user.is_superuser:
                review.delete()
                return Response({"message": "Комментарий удалён!"})
            return Response({"error": "Вы не можете удалить этот комментарий"})


# поиск ингредиента по названию
class IngredientSearchView(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        title = request.data["title"]
        ingredients_list = []
        if len(title) > 1:
            ingredients = Ingredient.objects.filter(other_names__contains = title.strip().lower())
            if ingredients:
                for ingredient in ingredients:
                    ingredients_list.append({f"{ingredient.id}": f"{ingredient.title}"})
        return Response({"result": ingredients_list})





