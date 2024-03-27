from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import timedelta, date
from dishapp.models import Dish, Cookware


# дата понедельника
def get_monday():
    # если сегодня не понедельник
    if(date.today().weekday() != 0):
        # дата понедельника = сегодня - дней(номер дня недели - 1) P.s. в питоне дни недели от 0 (пн) до 6 (вс)
        return date.today() - timedelta(days=date.today().weekday())
    else:
        return date.today()


# дата воскресенья
def get_sunday():
    # если сегодня не воскресенье
    if(date.today().weekday() != 6):
        # дата воскресенья = сегодня + дней(6 - номер дня недели) P.s. в питоне дни недели от 0 (пн) до 6 (вс)
        return date.today() + timedelta(days=6-date.today().weekday())
    else:
        return date.today()


# Меню
class Menu(models.Model):
    DIET = [
        ("usualdiet", 'Обычная'),
        ("weightloss", 'Для похудения'),
        ("weightgain", 'Для набора веса'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', help_text="Кому принадлежит меню", null=False)
    datestart = models.DateField(null=False, default=get_monday())
    dateend = models.DateField(null=False, default=get_sunday())
    info = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Информация', help_text="Дополнительная информация")
    diet = models.CharField(max_length=100, null=False, blank=False, choices=DIET, verbose_name='Диета', help_text="Выберите тип диеты", default="usualdiet")
    cookware = models.ManyToManyField(Cookware, blank=True, verbose_name="Посуда", help_text="Выберите посуду, которая у вас есть в наличии", related_name="menu")
    blacklist = models.ManyToManyField(Dish, blank=True, verbose_name='Исключенные блюда', help_text='Блюда, которые уже заменяли', related_name='blacklist')

    br_mon = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо завтрак пн', help_text="Блюдо завтрак пн", null=False, related_name='br_mon')
    lu_mon = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо обед пн', help_text="Блюдо обед пн", null=False, related_name='lu_mon')
    dn_mon = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо ужин пн', help_text="Блюдо ужин пн", null=False, related_name='dn_mon')

    br_tue = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо завтрак вт', help_text="Блюдо завтрак вт", null=False, related_name='br_tue')
    lu_tue = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо обед вт', help_text="Блюдо обед вт", null=False, related_name='lu_tue')
    dn_tue = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо ужин вт', help_text="Блюдо ужин вт", null=False, related_name='dn_tue')

    br_wed = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо завтрак ср', help_text="Блюдо завтрак ср", null=False, related_name='br_wed')
    lu_wed = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо обед ср', help_text="Блюдо обед ср", null=False, related_name='lu_wed')
    dn_wed = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо ужин ср', help_text="Блюдо ужин ср", null=False, related_name='dn_wed')

    br_thu = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо завтрак чт', help_text="Блюдо завтрак чт", null=False, related_name='br_thu')
    lu_thu = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо обед чт', help_text="Блюдо обед чт", null=False, related_name='lu_thu')
    dn_thu = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо ужин чт', help_text="Блюдо ужин чт", null=False, related_name='dn_thu')

    br_fri = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо завтрак пт', help_text="Блюдо завтрак пт", null=False, related_name='br_fri')
    lu_fri = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо обед пт', help_text="Блюдо обед пт", null=False, related_name='lu_fri')
    dn_fri = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо ужин пт', help_text="Блюдо ужин пт", null=False, related_name='dn_fri')

    br_sat = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо завтрак сб',help_text="Блюдо завтрак сб", null=False, related_name='br_sat')
    lu_sat = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо обед сб', help_text="Блюдо обед сб", null=False, related_name='lu_sat')
    dn_sat = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо ужин сб', help_text="Блюдо ужин сб", null=False, related_name='dn_sat')

    br_sun = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо завтрак вс',help_text="Блюдо завтрак вс", null=False, related_name='br_sun')
    lu_sun = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо обед вс', help_text="Блюдо обед вс", null=False, related_name='lu_sun')
    dn_sun = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо ужин вс', help_text="Блюдо ужин вс", null=False, related_name='dn_sun')
    objects = models.Manager()

    def __str__(self):
        return f'{self.owner}'

