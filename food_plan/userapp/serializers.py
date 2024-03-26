from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


# Без конфедициальной инфы
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'image', 'first_name', 'last_name']