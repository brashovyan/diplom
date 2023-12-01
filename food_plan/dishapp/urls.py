from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from dishapp.views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'cookwareviewset', CookwareViewSet)
router.register(r'ingredientviewset', IngredientViewSet)


urlpatterns = [
    path('cookware/', CookwareView.as_view()),
    path('cookware/<int:pk>/', CookwareDetailView.as_view()),
    path('ingredient/', IngredientView.as_view()),
    path('ingredient/<int:pk>/', IngredientDetailView.as_view()),
    path('ingredient_create/', IngredientCreateView.as_view()),
    path('create/', DishCreateView.as_view()),
    path('', DishListView.as_view()),
    path('<int:pk>/', DishDetailView.as_view()),
    path('', include(router.urls)),
]