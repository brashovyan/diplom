# Generated by Django 5.0 on 2024-02-27 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='dateend',
            field=models.DateField(default=datetime.datetime(2024, 3, 3, 14, 16, 47, 1254)),
        ),
        migrations.AlterField(
            model_name='menu',
            name='datestart',
            field=models.DateField(default=datetime.datetime(2024, 2, 26, 14, 16, 47, 1254)),
        ),
    ]
