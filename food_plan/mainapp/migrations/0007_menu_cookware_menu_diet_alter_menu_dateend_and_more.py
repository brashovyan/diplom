# Generated by Django 5.0 on 2024-03-25 20:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishapp', '0006_alter_ingredient_calories_and_more'),
        ('mainapp', '0006_menu_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='cookware',
            field=models.ManyToManyField(blank=True, help_text='Выберите посуду, которая у вас есть в наличии', related_name='menu', to='dishapp.cookware', verbose_name='Посуда'),
        ),
        migrations.AddField(
            model_name='menu',
            name='diet',
            field=models.CharField(choices=[('usualdiet', 'Обычная'), ('weightloss', 'Для похудения'), ('weightgain', 'Для набора веса')], default='usualdiet', help_text='Выберите тип диеты', max_length=100, verbose_name='Диета'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='dateend',
            field=models.DateField(default=datetime.date(2024, 3, 31)),
        ),
        migrations.AlterField(
            model_name='menu',
            name='datestart',
            field=models.DateField(default=datetime.date(2024, 3, 25)),
        ),
    ]
