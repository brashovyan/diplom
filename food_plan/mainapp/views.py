import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import Group
from datetime import date
from dishapp.models import *
from django.db.models import Q
import random


# сортировка по посуде и ингредиентам
def CookwareIngredientSort(dishes, cookware_list, user):
    try:
        # список для дальнейшей сортировки
        dishes_list = []

        # сортировка по посуде
        # если пользователь не указал посуду, значит эта сортировка игнорируется
        if len(cookware_list) > 0:
            for dish in dishes:
                # получаю всю посуду в блюде (если у блюда нет ни одной посуды, то я его игнорирую)
                flag = True
                counter = 0
                for dish_cookware in dish.cookware.all():
                    counter += 1
                    # проверяю, что каждая посуда для блюда есть в списке фильтра
                    if dish_cookware.id not in cookware_list:
                        flag = False
                        break
                # если вся посуда есть, то это блюдо нам подходит
                if flag and counter > 0:
                    dishes_list.append(dish)
        else:
            for dish in dishes:
                dishes_list.append(dish)

        # проверка ингредиентов
        # получаю список забаненных пользователем ингредиентов
        ingredients_in_ban_list = []
        for ingredient in user.user_ban_ingredient.all():
            ingredients_in_ban_list.append(ingredient.id)

        dishes_list2 = []
        for dish in dishes_list:
            # получаю все ингредиенты блюда (если ингредиентов нет - пропуск)
            flag = True
            counter = 0
            for ingredient_dish in DishIngredients.objects.filter(dish=dish):
                counter += 1
                # проверяю есть ли каждый отдельный ингредиент в списке банов
                if ingredient_dish.ingredient.id in ingredients_in_ban_list:
                    flag = False
                    break
            # если все ингредиенты разрешены, то это блюдо нам подходит
            if flag and counter > 0:
                dishes_list2.append(dish)
        dishes_list.clear()

        # В итоге получаю список блюд, которые подходят под все условия
        return dishes_list2
    except:
        # Если в сортировке что-то сломалось
        return -1

# Алгоритм создания меню
class AlgorithmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # получаю данные с фронта
            diet = request.data["diet"]
            cookware = request.data["cookware"]

            # сначала высчитываем норму кбжу юзера
            user = request.user
            today = date.today()
            age = int(today.year - user.date_of_birth.year - ((today.month, today.day) < (user.date_of_birth.month, user.date_of_birth.day)))
            coef = 1.375 # Коэфициент физической активности
            calories = 0
            proteins = 0
            fats = 0
            carbohydrates = 0
            if(user.sex == "M"):
                calories = (10 * user.weight + 6.25 * user.height - 5 * age + 5) * coef
            else:
                calories = (10 * user.weight + 6.25 * user.height - 5 * age - 161) * coef

            if(diet == "usual"):
                proteins = (0.15 * calories) / 4
                fats = (0.3 * calories) / 9
                carbohydrates = (0.55 * calories) / 4

            elif(diet == "weightloss"):
                calories = calories * 0.85
                proteins = (0.20 * calories) / 4
                fats = (0.35 * calories) / 9
                carbohydrates = (0.45 * calories) / 4

            elif (diet == "weightgain"):
                calories = calories * 1.15
                proteins = (0.25 * calories) / 4
                fats = (0.25 * calories) / 9
                carbohydrates = (0.5 * calories) / 4

            else:
                calories = 0
                proteins = 0
                fats = 0
                carbohydrates = 0

            # костыль, потому что я список с фронта получаю в виде строки
            cookware_list = []
            for c in cookware:
                try:
                    c = int(c)
                    cookware_list.append(c)
                except:
                    pass

            # сам алгоритм
            if calories > 0 and proteins > 0 and fats > 0 and carbohydrates > 0:
                print(f'Вам нужно {calories} калорий, {proteins}г белков, {fats}г жиров, {carbohydrates}г углеводов в день')
                if(diet=="usual"):
                    criterion_diet =  Q(usualdiet=True)
                elif(diet=="weightloss"):
                    criterion_diet = Q(weightloss=True)
                elif(diet=="weightgain"):
                    criterion_diet = Q(weightgain=True)

                try:
                    # получаю все завтраки, обеды и ужины, которые удовлетворяют нашим условиям
                    # подходит для завтрака, диета, не в дизлайках
                    breakfasts_all = Dish.objects.filter(Q(breakfast=True) & criterion_diet & ~Q(id__in=user.dish_dislikes.all()))
                    # сортирую по посуде и ингредиентам
                    breakfasts = CookwareIngredientSort(breakfasts_all, cookware_list, user)
                    # дальше аналогично
                    lunchs_all = Dish.objects.filter(Q(lunch=True) & criterion_diet & ~Q(id__in=user.dish_dislikes.all()))
                    lunchs = CookwareIngredientSort(lunchs_all, cookware_list, user)

                    dinners_all = Dish.objects.filter(Q(dinner=True) & criterion_diet & ~Q(id__in=user.dish_dislikes.all()))
                    dinners = CookwareIngredientSort(dinners_all, cookware_list, user)

                    for breakfast in breakfasts:
                        print(breakfast.title)
                    print('-----------------')
                    for lunch in lunchs:
                        print(lunch.title)
                    print('-----------------')
                    for dinner in dinners:
                        print(dinner.title)
                    print('-----------------')

                    # дальше надо проверить, что у нас минимум по 7 завтраков, обедов и ужинов (иначе рацион на неделю не составить)
                    if len(breakfasts) > 6 and len(lunchs) > 6 and len(dinners) > 6:

                        # список блюд в меню
                        menu_list = []

                        # заполняем понедельник
                        # беру рандомные завтрак, обед и ужин
                        breakfast = random.choice(breakfasts)
                        lunch = random.choice(lunchs)
                        dinner = random.choice(dinners)

                        # и удаляю то, что взял из списка

                        # пока не удовлетворю все условия, буду крутиться тут
                        flag = False
                        while flag == False:
                            # проверяю норму калорий (± 100)
                            calories_sum = breakfast.calories + lunch.calories + dinner.calories
                            if calories - 100 < calories_sum < calories + 100:
                                # далее норма белков, жиров, углеводов (± 10)
                                pass

                    else:
                        # недостаточно блюд для меню
                        print("недостаточно блюд для меню")
                        pass

                except:
                    # Если алгоритм не сработал
                    pass

            else:
                # Если у нас не получилось сосчитать кбжу
                pass

        except Exception as error:
            # Если непредвиденная ошибка
            print(error)

        return Response({'Message': 'Hello, world!'})



