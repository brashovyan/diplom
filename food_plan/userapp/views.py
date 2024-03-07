import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import Group
from dishapp.models import Ingredient
from django.shortcuts import get_object_or_404
from .serializers import *


""" Смена пароля """
    # email = request.user
    # user = User.objects.get(email=email)
    # # требования к паролю: 8 символов и больше, не распространён (qwertyui, password не катит),
    # # а так могут быть только буквы (но не только цифры), необязательны спецсимволы, необязательны заглавные
    # user.set_password('artik812')
    # user.save()


# этот метод вызывается после регистрации юзера
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # после регистрации я юзеру сразу даю обычную роль
        group, created = Group.objects.get_or_create(name='usual')
        instance.groups.add(group)


# автоматическое удаление картинки при удалении юзера
@receiver(post_delete, sender=User)
def delete_article(sender, instance, **kwargs):
    try:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)
    except:
        pass


# автоматическое удаление картинки, если её изменили
@receiver(pre_save, sender=User)
def pre_save_image(sender, instance, *args, **kwargs):
    try:
        old_img = User.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


# любой авторизованный юзер может добавить в черный список ингредиент (чтобы он не попадался в блюдах) по айди
class BanIngredientView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            ingredient = get_object_or_404(Ingredient, pk=pk)
            ingredient.users_ban.add(request.user)
            # получить все ингредиенты, которые забанил юзер
            #print(request.user.user_ban_ingredient.all())
            return Response({"message": f'Больше {ingredient.title} не будет попадаться в блюдах в вашем меню'})


# Любой авторизованный юзер может снова разрешить ингредиент
class AllowIngredientView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            ingredient = get_object_or_404(Ingredient, pk=pk)
            ingredient.users_ban.remove(request.user)
            return Response({"message": f'{ingredient.title} снова будет появляться в блюдах в вашем меню'})


# Кастомное получение информации о себе для фронта (шапка, авторизация)
class UserMeFrontView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        groups = request.user.groups.all()
        user_groups = []
        for group in groups:
            user_groups.append(group.name)
        if "administrator" in user_groups or request.user.is_superuser:
            user_group = "administrator"
        elif "moderator" in user_groups:
            user_group = "moderator"
        else:
            user_group = "usual"
        data = UserSerializer(request.user, many=False, context={"request": request}).data
        data['user_group'] = user_group
        return Response(data)