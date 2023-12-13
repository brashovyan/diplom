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
from .tasks import *


class IndexView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """ Смена пароля """
        # email = request.user
        # user = User.objects.get(email=email)
        # # требования к паролю: 8 символов и больше, не распространён (qwertyui, password не катит),
        # # а так могут быть только буквы (но не только цифры), необязательны спецсимволы, необязательны заглавные
        # user.set_password('artik812')
        celery_test.delay()
  
        return Response({'Message': 'Hello, world!'})
