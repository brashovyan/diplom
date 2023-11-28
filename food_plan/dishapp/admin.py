from django.contrib import admin
from .models import Ingredient, Cookware, Dish, Review, DishIngredients


admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(Cookware)
admin.site.register(Review)
admin.site.register(DishIngredients)