from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import Group


# этот метод вызывается после регистрации юзера
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # после регистрации я юзеру сразу даю обычную роль
        group, created = Group.objects.get_or_create(name='usual')
        instance.groups.add(group)


class IndexView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response({'Message': 'Hello, world!'})
