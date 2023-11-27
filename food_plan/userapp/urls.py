from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from userapp.views import *
from rest_framework import routers


urlpatterns = [
    #path('', IndexView.as_view()),
]