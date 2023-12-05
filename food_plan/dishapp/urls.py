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
    path('update/<int:pk>/', DishUpdateView.as_view()),
    path('delete/<int:pk>/', DishDeleteView.as_view()),
    path('like/<int:pk>/', DishLikeView.as_view()),
    path('dislike/<int:pk>/', DishDislikeView.as_view()), # пк блюда
    path('clear_like/<int:pk>/', DishClearLikeView.as_view()), # пк блюда
    path('create_review/<int:pk>/', ReviewCreateView.as_view()), # пк блюда
    path('update_delete_review/<int:pk>/', ReviewUpdateDeleteView.as_view()), # пк отзыва
    path('', DishListView.as_view()),
    path('<int:pk>/', DishDetailView.as_view()), # пк блюда
    path('get_actual_price/<int:pk>/', DishActualPriceView.as_view()), # пк блюда
    path('', include(router.urls)),

]