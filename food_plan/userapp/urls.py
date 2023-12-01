from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from userapp.views import *
from rest_framework import routers


urlpatterns = [
    path('ban_ingredient/<int:pk>/', BanIngredientView.as_view()),
    path('allow_ingredient/<int:pk>/', AllowIngredientView.as_view()),
]