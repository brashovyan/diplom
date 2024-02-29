from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


# ингридиенты со списком банов
class Ingredient(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название", help_text="Введите название", null=False)
    price = models.FloatField(default=0, verbose_name="Цена (за шт/кг)", help_text="Введите цену (за шт/кг)", null=False)
    last_update_price = models.DateField(null=True, blank=True)
    other_names = models.TextField(verbose_name="Другие названия", help_text="Введите другие названия", null=True)
    users_ban = models.ManyToManyField(User, help_text='Выберите пользователей, которые не хотят видеть этот ингредиент в блюдах', verbose_name='Пользователи, которые не хотят видеть этот ингредиент в блюдах', blank=True, related_name='user_ban_ingredient')
    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'


# Посуда
class Cookware(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название", help_text="Введите название", null=False)
    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'


# Комментарии
class Review(models.Model):
    content = models.TextField(verbose_name="Отзыв", help_text="Напишите отзыв", null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', help_text="Автор отзыва", null=False, related_name='user_review')
    date_review = models.DateTimeField(auto_now_add=True, null=False)
    objects = models.Manager()

    def __str__(self):
        return f'{self.creator}'


# Блюдо со списком лайков, дизлайков
class Dish(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название", help_text="Введите название", null=False)
    description = models.CharField(max_length=1000, verbose_name="Краткое описание", help_text="Введите краткое описание", null=False)
    proteins = models.FloatField(default=0, null=False, verbose_name="Белки, грамм", help_text="Введите белки в граммах")
    fats = models.FloatField(default=0, null=False, verbose_name="Жиры, грамм", help_text="Введите жиры в граммах")
    carbohydrates = models.FloatField(default=0, null=False, verbose_name="Углеводы, грамм", help_text="Введите углеводы в граммах")
    calories = models.FloatField(default=0, null=False, verbose_name="Калории, ккал", help_text="Введите калории, ккал")
    breakfast = models.BooleanField(verbose_name="Подходит для завтрака", help_text="Подходит для завтрака", null=False, default=False)
    lunch = models.BooleanField(verbose_name="Подходит для обеда", help_text="Подходит для обеда", null=False, default=False)
    dinner = models.BooleanField(verbose_name="Подходит для ужина", help_text="Подходит для ужина", null=False, default=False)
    usualdiet = models.BooleanField(verbose_name="Подходит для обычного питания", help_text="Подходит для обычного питания", null=False, default=False)
    weightloss = models.BooleanField(verbose_name="Подходит для похудения", help_text="Подходит для похудения", null=False, default=False)
    weightgain = models.BooleanField(verbose_name="Подходит для набора веса", help_text="Подходит для набора веса", null=False, default=False)
    recipe = models.TextField(null=False, verbose_name="Рецепт", help_text="Напишите рецепт приготовления")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='dish_creator')
    time = models.CharField(max_length=100, verbose_name="Время готовки", help_text="Укажите время готовки", null=False, default="Не указано")
    likes = models.ManyToManyField(User, help_text='Выберите пользователей, которым нравится это блюдо', verbose_name='Пользователи, которым нравится это блюдо', blank=True, related_name='dish_likes')
    dislikes = models.ManyToManyField(User, help_text='Выберите пользователей, которым ненравится это блюдо',verbose_name='Пользователи, которым ненравится это блюдо', blank=True, related_name='dish_dislikes')
    modercheck = models.BooleanField(null=False, default=False, verbose_name="Проверено модератором", help_text="Проверено модератором")
    in_algorithm = models.BooleanField(null=False, default=False, verbose_name="Блюдо в алгоритме", help_text="Будет ли это блюдо учитываться алгоритмом")
    cookware = models.ManyToManyField(Cookware, blank=True, verbose_name="Необходимая посуда", help_text="Выберите необходимую посуду для готовки", related_name="cookware")
    mainphoto = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите главное фото блюда")
    photo1 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    photo2 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    photo3 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    photo4 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    photo5 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    photo6 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    photo7 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    photo8 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    photo9 = models.ImageField(upload_to='dish/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото блюда")
    reviews = models.ManyToManyField('Review', blank=True, verbose_name='Отзывы')
    date_create = models.DateTimeField(auto_now_add=True, null=False)
    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'


class DishIngredients(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=False, verbose_name="Блюдо", help_text="Выберите блюдо", related_name="dish")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=False, verbose_name="Ингредиент", help_text="Выберите ингредиент", related_name='ingregient')
    count = models.CharField(max_length=100, null=False, default="Не указано", verbose_name="Кол-во", help_text="Укажите кол-во")
    objects = models.Manager()

    def __str__(self):
        return f'{self.dish}'

