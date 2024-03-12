from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from .models import *
from userapp.serializers import UserSerializer
from dishapp.serializers import DishListSerializer


class MenuDetailSerializer(serializers.ModelSerializer):
    datestart = serializers.DateField()
    dateend = serializers.DateField()
    owner = UserSerializer(read_only=True, many=False)
    br_mon = DishListSerializer(read_only=True, many=False)
    lu_mon = DishListSerializer(read_only=True, many=False)
    dn_mon = DishListSerializer(read_only=True, many=False)
    br_tue = DishListSerializer(read_only=True, many=False)
    lu_tue = DishListSerializer(read_only=True, many=False)
    dn_tue = DishListSerializer(read_only=True, many=False)
    br_wed = DishListSerializer(read_only=True, many=False)
    lu_wed = DishListSerializer(read_only=True, many=False)
    dn_wed = DishListSerializer(read_only=True, many=False)
    br_thu = DishListSerializer(read_only=True, many=False)
    lu_thu = DishListSerializer(read_only=True, many=False)
    dn_thu = DishListSerializer(read_only=True, many=False)
    br_fri = DishListSerializer(read_only=True, many=False)
    lu_fri = DishListSerializer(read_only=True, many=False)
    dn_fri = DishListSerializer(read_only=True, many=False)
    br_sat = DishListSerializer(read_only=True, many=False)
    lu_sat = DishListSerializer(read_only=True, many=False)
    dn_sat = DishListSerializer(read_only=True, many=False)
    br_sun = DishListSerializer(read_only=True, many=False)
    lu_sun = DishListSerializer(read_only=True, many=False)
    dn_sun = DishListSerializer(read_only=True, many=False)

    class Meta:
        model = Menu
        fields = "__all__"