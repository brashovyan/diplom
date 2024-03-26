from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from mainapp.views import *
from rest_framework import routers


urlpatterns = [
    path('create_menu/', AlgorithmView.as_view()),
    path('get_menu/', GetMenuView.as_view()),
    path('replace/', ReplaceView.as_view()),
]