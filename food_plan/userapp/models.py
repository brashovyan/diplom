from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager


# Убираю у юзера поле username, и делаю вместо него email. Логин через email
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    SEX_CHOISE=[
        ('M', "Мужской"),
        ('F', "Женский"),
    ]

    username = None
    email = models.EmailField(unique=True, null=False)
    USERNAME_FIELD = 'email'

    # дополняем к обычному джанговскому юзеру дополнительные поля
    height = models.FloatField(null=False, blank=False, verbose_name="Рост (см)", help_text="Введите ваш рост в сантиметрах")
    weight = models.FloatField(null=False, blank=False, verbose_name="Вес (кг)", help_text="Введите ваш вес в килограммах")
    date_of_birth = models.DateField(null=False, blank=False, verbose_name="Дата рождения", help_text="Введите вашу дату рождения")
    sex = models.CharField(null=False, blank=False, choices=SEX_CHOISE, max_length=1, verbose_name="Пол", help_text="Выберите пол")
    image = models.ImageField(upload_to='user/', blank=True, null=True, verbose_name="Фото", help_text="Выберите фото профиля")

    # поля, с которыми мы в будущем хотим работать (кроме пароля и юзернейма)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'height', 'weight', 'date_of_birth', 'sex', 'image']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


