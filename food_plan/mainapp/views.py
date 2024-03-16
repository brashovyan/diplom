from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()
from dishapp.models import *
from django.db.models import Q
import random
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework import generics, viewsets


# сортировка по посуде и ингредиентам
def CookwareIngredientSort(dishes, cookware_list, user):
    try:
        # список для дальнейшей сортировки
        dishes_list = []

        # сортировка по посуде. Eсли пользователь не указал посуду, значит эта сортировка игнорируется
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

        # проверка ингредиентов. Получаю список забаненных пользователем ингредиентов
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


# проверка на лучшее сочетание (суммарная ошибка)
def CheckTop(top, breakfast, lunch, dinner, calories_sum, proteins_sum, fats_sum, carbohydrates_sum, calories, fats, proteins, carbohydrates):
    top_calories_sum = top[0].calories + top[1].calories + top[2].calories
    top_proteins_sum = top[0].proteins + top[1].proteins + top[2].proteins
    top_fats_sum = top[0].fats + top[1].fats + top[2].fats
    top_carbohydrates_sum = top[0].carbohydrates + top[1].carbohydrates + top[2].carbohydrates
    top_error = abs(calories - top_calories_sum) + abs(proteins - top_proteins_sum) + abs(fats - top_fats_sum) + abs(carbohydrates - top_carbohydrates_sum)
    now_error = abs(calories - calories_sum) + abs(proteins - proteins_sum) + abs(fats - fats_sum) + abs(carbohydrates - carbohydrates_sum)
    if top_error > now_error:
        top = []
        top.append(breakfast)
        top.append(lunch)
        top.append(dinner)
    return top


# генерация сочетания завтрака, обеда и ужина
def DayGeneration(breakfasts, lunchs, dinners, calories, proteins, fats, carbohydrates):
    # список блюд на день
    menu_list = []

    # примерная работа алгоритма:
    # пытаюсь зарандомить идеал (0 промахов) n кол-во раз
    # если в итоге не получился идеал, то беру самое лучшее (топовое) сочетание

    top_1 = [] # угадал калории, но одна ошибка
    top_2 = [] # угадал калории, но две ошибки
    top_3 = [] # угадал калории, но три ошибки
    top_4 = [] # не угадал калории, но в остальном без ошибок
    top_5 = [] # не угадал калории, и ещё одна ошибка
    top_6 = [] # не угадал калории, и ёще две ошибки
    top_7 = [] # вообще ничего не угадал
    count = 0
    combinations = []

    while count < 500:
        count += 1

        # беру рандомные завтрак, обед и ужин
        count2 = 0
        while count2 < 100:
            count2 += 1
            breakfast = random.choice(breakfasts)
            lunch = random.choice(lunchs)
            dinner = random.choice(dinners)
            combination = [lunch.id, breakfast.id, dinner.id]

            # все блюда разные
            if breakfast.id != lunch.id and breakfast.id != dinner.id and lunch.id != dinner.id:
                # такого сочетания ещё не было
                if combination not in combinations:
                    combinations.append(combination)
                    break
            combinations.append(combination)

        # считаю суммарные кбжу
        calories_sum = breakfast.calories + lunch.calories + dinner.calories
        proteins_sum = breakfast.proteins + lunch.proteins + dinner.proteins
        fats_sum = breakfast.fats + lunch.fats + dinner.fats
        carbohydrates_sum = breakfast.carbohydrates + lunch.carbohydrates + dinner.carbohydrates

        # кол-во попаданий
        coincidences = 0
        # совпали ли калории
        calories_flag = False

        if calories - 100 < calories_sum < calories + 100:
            coincidences += 1
            calories_flag = True
        if proteins - 10 < proteins_sum < proteins + 10:
            coincidences += 1
        if fats - 10 < fats_sum < fats + 10:
            coincidences += 1
        if carbohydrates - 10 < carbohydrates_sum < carbohydrates + 10:
            coincidences += 1

        # идеальное совпадение
        if coincidences == 4:
            menu_list.append(breakfast)
            menu_list.append(lunch)
            menu_list.append(dinner)
            return menu_list

        # Самое главное, чтобы сперва совпали калории
        if calories_flag:
            # один промах
            if coincidences == 3:
                if len(top_1) > 0:
                    top_1 = CheckTop(top_1, breakfast, lunch, dinner, calories_sum, proteins_sum, fats_sum, carbohydrates_sum, calories, fats, proteins, carbohydrates)
                else:
                    top_1 = []
                    top_1.append(breakfast)
                    top_1.append(lunch)
                    top_1.append(dinner)

            # два промаха
            elif coincidences == 2:
                if len(top_2) > 0:
                    top_2 = CheckTop(top_2, breakfast, lunch, dinner, calories_sum, proteins_sum, fats_sum, carbohydrates_sum, calories, fats, proteins, carbohydrates)
                else:
                    top_2 = []
                    top_2.append(breakfast)
                    top_2.append(lunch)
                    top_2.append(dinner)

            # три промаха
            elif coincidences == 1:
                if len(top_3) > 0:
                    top_3 = CheckTop(top_3, breakfast, lunch, dinner, calories_sum, proteins_sum, fats_sum, carbohydrates_sum, calories, fats, proteins, carbohydrates)
                else:
                    top_3 = []
                    top_3.append(breakfast)
                    top_3.append(lunch)
                    top_3.append(dinner)

        # не угадали калории
        else:
            # один промах
            if coincidences == 3:
                if len(top_4) > 0:
                    top_4 = CheckTop(top_4, breakfast, lunch, dinner, calories_sum, proteins_sum, fats_sum, carbohydrates_sum, calories, fats, proteins, carbohydrates)
                else:
                    top_4 = []
                    top_4.append(breakfast)
                    top_4.append(lunch)
                    top_4.append(dinner)

            # два промаха
            elif coincidences == 2:
                if len(top_5) > 0:
                    top_5 = CheckTop(top_5, breakfast, lunch, dinner, calories_sum, proteins_sum, fats_sum, carbohydrates_sum, calories, fats, proteins, carbohydrates)
                else:
                    top_5 = []
                    top_5.append(breakfast)
                    top_5.append(lunch)
                    top_5.append(dinner)

            # три промаха
            elif coincidences == 1:
                if len(top_6) > 0:
                    top_6 = CheckTop(top_6, breakfast, lunch, dinner, calories_sum, proteins_sum, fats_sum, carbohydrates_sum, calories, fats, proteins, carbohydrates)
                else:
                    top_6 = []
                    top_6.append(breakfast)
                    top_6.append(lunch)
                    top_6.append(dinner)

            # ничего не угадал
            elif coincidences == 0:
                if len(top_7) > 0:
                    top_7 = CheckTop(top_7, breakfast, lunch, dinner, calories_sum, proteins_sum, fats_sum, carbohydrates_sum, calories, fats, proteins, carbohydrates)
                else:
                    top_7 = []
                    top_7.append(breakfast)
                    top_7.append(lunch)
                    top_7.append(dinner)


    if len(top_1) > 0:
        menu_list.append(top_1[0])
        menu_list.append(top_1[1])
        menu_list.append(top_1[2])
        return menu_list

    elif len(top_2) > 0:
        menu_list.append(top_2[0])
        menu_list.append(top_2[1])
        menu_list.append(top_2[2])
        return menu_list

    elif len(top_3) > 0:
        menu_list.append(top_3[0])
        menu_list.append(top_3[1])
        menu_list.append(top_3[2])
        return menu_list

    elif len(top_4) > 0:
        menu_list.append(top_4[0])
        menu_list.append(top_4[1])
        menu_list.append(top_4[2])
        return menu_list

    elif len(top_5) > 0:
        menu_list.append(top_5[0])
        menu_list.append(top_5[1])
        menu_list.append(top_5[2])
        return menu_list

    elif len(top_6) > 0:
        menu_list.append(top_6[0])
        menu_list.append(top_6[1])
        menu_list.append(top_6[2])
        return menu_list

    elif len(top_7) > 0:
        menu_list.append(top_7[0])
        menu_list.append(top_7[1])
        menu_list.append(top_7[2])
        return menu_list

    else:
        return -1


# Алгоритм создания меню
class AlgorithmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # получаю данные с фронта
            diet = request.data["diet"]
            cookware = request.data.getlist("cookware")

            # сначала высчитываем норму кбжу юзера
            coef = 1
            user = request.user
            if user.physical_activity == "minimum":
                coef = 1.2
            elif user.physical_activity == "training3":
                coef = 1.375
            elif user.physical_activity == "training5":
                coef = 1.55
            elif user.physical_activity == "intensetraining5":
                coef = 1.7
            elif user.physical_activity == "maximum":
                coef = 1.9
            today = date.today()
            age = int(today.year - user.date_of_birth.year - ((today.month, today.day) < (user.date_of_birth.month, user.date_of_birth.day)))
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

            cookware_list = []
            for c in cookware:
                c = int(c)
                cookware_list.append(c)

            # сам алгоритм
            if calories > 0 and proteins > 0 and fats > 0 and carbohydrates > 0:
                if(diet=="usual"):
                    criterion_diet = Q(usualdiet=True)
                elif(diet=="weightloss"):
                    criterion_diet = Q(weightloss=True)
                elif(diet=="weightgain"):
                    criterion_diet = Q(weightgain=True)

                try:
                    # получаю все завтраки, обеды и ужины, которые удовлетворяют нашим условиям (подходит для завтрака, диета, не в дизлайках)
                    breakfasts_all = Dish.objects.filter(Q(breakfast=True) & criterion_diet & ~Q(id__in=user.dish_dislikes.all()) & Q(in_algorithm=True))
                    # сортирую по посуде и ингредиентам
                    breakfasts = CookwareIngredientSort(breakfasts_all, cookware_list, user)

                    # дальше аналогично
                    lunchs_all = Dish.objects.filter(Q(lunch=True) & criterion_diet & ~Q(id__in=user.dish_dislikes.all()) & Q(in_algorithm=True))
                    lunchs = CookwareIngredientSort(lunchs_all, cookware_list, user)

                    dinners_all = Dish.objects.filter(Q(dinner=True) & criterion_diet & ~Q(id__in=user.dish_dislikes.all()) & Q(in_algorithm=True))
                    dinners = CookwareIngredientSort(dinners_all, cookware_list, user)

                    # дальше надо проверить, что у нас минимум по 7 завтраков, обедов и ужинов (иначе рацион на неделю не составить)
                    if len(breakfasts) > 6 and len(lunchs) > 6 and len(dinners) > 6:
                        # генерирую каждый день, и удаляю выбранные блюда из списка, чтобы они не попались снова
                        monday = DayGeneration(breakfasts, lunchs, dinners, calories, proteins, fats, carbohydrates)
                        if monday[0] in breakfasts:
                            breakfasts.remove(monday[0])
                        if monday[0] in lunchs:
                            lunchs.remove(monday[0])
                        if monday[0] in dinners:
                            dinners.remove(monday[0])
                        if monday[1] in breakfasts:
                            breakfasts.remove(monday[1])
                        if monday[1] in lunchs:
                            lunchs.remove(monday[1])
                        if monday[1] in dinners:
                            dinners.remove(monday[1])
                        if monday[2] in breakfasts:
                            breakfasts.remove(monday[2])
                        if monday[2] in lunchs:
                            lunchs.remove(monday[2])
                        if monday[2] in dinners:
                            dinners.remove(monday[2])

                        tuesday = DayGeneration(breakfasts, lunchs, dinners, calories, proteins, fats, carbohydrates)
                        if tuesday[0] in breakfasts:
                            breakfasts.remove(tuesday[0])
                        if tuesday[0] in lunchs:
                            lunchs.remove(tuesday[0])
                        if tuesday[0] in dinners:
                            dinners.remove(tuesday[0])
                        if tuesday[1] in breakfasts:
                            breakfasts.remove(tuesday[1])
                        if tuesday[1] in lunchs:
                            lunchs.remove(tuesday[1])
                        if tuesday[1] in dinners:
                            dinners.remove(tuesday[1])
                        if tuesday[2] in breakfasts:
                            breakfasts.remove(tuesday[2])
                        if tuesday[2] in lunchs:
                            lunchs.remove(tuesday[2])
                        if tuesday[2] in dinners:
                            dinners.remove(tuesday[2])

                        wednesday = DayGeneration(breakfasts, lunchs, dinners, calories, proteins, fats, carbohydrates)
                        if wednesday[0] in breakfasts:
                            breakfasts.remove(wednesday[0])
                        if wednesday[0] in lunchs:
                            lunchs.remove(wednesday[0])
                        if wednesday[0] in dinners:
                            dinners.remove(wednesday[0])
                        if wednesday[1] in breakfasts:
                            breakfasts.remove(wednesday[1])
                        if wednesday[1] in lunchs:
                            lunchs.remove(wednesday[1])
                        if wednesday[1] in dinners:
                            dinners.remove(wednesday[1])
                        if wednesday[2] in breakfasts:
                            breakfasts.remove(wednesday[2])
                        if wednesday[2] in lunchs:
                            lunchs.remove(wednesday[2])
                        if wednesday[2] in dinners:
                            dinners.remove(wednesday[2])

                        thursday = DayGeneration(breakfasts, lunchs, dinners, calories, proteins, fats, carbohydrates)
                        if thursday[0] in breakfasts:
                            breakfasts.remove(thursday[0])
                        if thursday[0] in lunchs:
                            lunchs.remove(thursday[0])
                        if thursday[0] in dinners:
                            dinners.remove(thursday[0])
                        if thursday[1] in breakfasts:
                            breakfasts.remove(thursday[1])
                        if thursday[1] in lunchs:
                            lunchs.remove(thursday[1])
                        if thursday[1] in dinners:
                            dinners.remove(thursday[1])
                        if thursday[2] in breakfasts:
                            breakfasts.remove(thursday[2])
                        if thursday[2] in lunchs:
                            lunchs.remove(thursday[2])
                        if thursday[2] in dinners:
                            dinners.remove(thursday[2])

                        friday = DayGeneration(breakfasts, lunchs, dinners, calories, proteins, fats, carbohydrates)
                        if friday[0] in breakfasts:
                            breakfasts.remove(friday[0])
                        if friday[0] in lunchs:
                            lunchs.remove(friday[0])
                        if friday[0] in dinners:
                            dinners.remove(friday[0])
                        if friday[1] in breakfasts:
                            breakfasts.remove(friday[1])
                        if friday[1] in lunchs:
                            lunchs.remove(friday[1])
                        if friday[1] in dinners:
                            dinners.remove(friday[1])
                        if friday[2] in breakfasts:
                            breakfasts.remove(friday[2])
                        if friday[2] in lunchs:
                            lunchs.remove(friday[2])
                        if friday[2] in dinners:
                            dinners.remove(friday[2])

                        saturday = DayGeneration(breakfasts, lunchs, dinners, calories, proteins, fats, carbohydrates)
                        if saturday[0] in breakfasts:
                            breakfasts.remove(saturday[0])
                        if saturday[0] in lunchs:
                            lunchs.remove(saturday[0])
                        if saturday[0] in dinners:
                            dinners.remove(saturday[0])
                        if saturday[1] in breakfasts:
                            breakfasts.remove(saturday[1])
                        if saturday[1] in lunchs:
                            lunchs.remove(saturday[1])
                        if saturday[1] in dinners:
                            dinners.remove(saturday[1])
                        if saturday[2] in breakfasts:
                            breakfasts.remove(saturday[2])
                        if saturday[2] in lunchs:
                            lunchs.remove(saturday[2])
                        if saturday[2] in dinners:
                            dinners.remove(saturday[2])

                        sunday = DayGeneration(breakfasts, lunchs, dinners, calories, proteins, fats, carbohydrates)
                        if sunday[0] in breakfasts:
                            breakfasts.remove(sunday[0])
                        if sunday[0] in lunchs:
                            lunchs.remove(sunday[0])
                        if sunday[0] in dinners:
                            dinners.remove(sunday[0])
                        if sunday[1] in breakfasts:
                            breakfasts.remove(sunday[1])
                        if sunday[1] in lunchs:
                            lunchs.remove(sunday[1])
                        if sunday[1] in dinners:
                            dinners.remove(sunday[1])
                        if sunday[2] in breakfasts:
                            breakfasts.remove(sunday[2])
                        if sunday[2] in lunchs:
                            lunchs.remove(sunday[2])
                        if sunday[2] in dinners:
                            dinners.remove(sunday[2])

                        # проверяю есть ли уже меню на эту неделю
                        monday_date = get_monday()
                        check_menu = Menu.objects.filter(datestart=monday_date, owner=request.user)

                        # если есть, то я удаляю старое меню (потому что на неделе может быть только одно меню)
                        if len(check_menu) > 0:
                            check_menu.delete()

                        menu = Menu.objects.create(
                            owner = request.user,
                            info = f'Вам нужно {round(calories, 2)} калорий, {round(proteins, 2)}г белков, {round(fats, 2)}г жиров, {round(carbohydrates, 2)}г углеводов в день',
                            br_mon = monday[0],
                            lu_mon = monday[1],
                            dn_mon = monday[2],

                            br_tue = tuesday[0],
                            lu_tue = tuesday[1],
                            dn_tue = tuesday[2],

                            br_wed = wednesday[0],
                            lu_wed = wednesday[1],
                            dn_wed = wednesday[2],

                            br_thu = thursday[0],
                            lu_thu = thursday[1],
                            dn_thu = thursday[2],

                            br_fri = friday[0],
                            lu_fri = friday[1],
                            dn_fri = friday[2],

                            br_sat = saturday[0],
                            lu_sat = saturday[1],
                            dn_sat = saturday[2],

                            br_sun = sunday[0],
                            lu_sun = sunday[1],
                            dn_sun = sunday[2],
                        )
                        return Response(MenuDetailSerializer(menu, many=False, context={"request": request}).data)

                    else:
                        # недостаточно блюд для меню
                        return Response({"error": "Недостаточно блюд для меню"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                except Exception as error:
                    # Если алгоритм не сработал
                    return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                # Если у нас не получилось сосчитать кбжу
                return Response({"error": "Не получилось сосчитать норму КБЖУ. Убедитесь, что вы выбрали диету, и в личном кабинете указаны ваши данные"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as error:
            # Если непредвиденная ошибка
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Получить меню на эту неделю
class GetMenuView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuDetailSerializer

    def get_queryset(self):
        return Menu.objects.filter(datestart=get_monday(), owner=self.request.user)


