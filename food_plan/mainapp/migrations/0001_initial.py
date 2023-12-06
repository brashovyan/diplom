# Generated by Django 4.2.7 on 2023-12-06 17:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dishapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datestart', models.DateField(default=datetime.datetime(2023, 12, 4, 17, 28, 6, 639890))),
                ('dateend', models.DateField(default=datetime.datetime(2023, 12, 10, 17, 28, 6, 639890))),
                ('br_fri', models.ForeignKey(help_text='Блюдо завтрак пт', on_delete=django.db.models.deletion.CASCADE, related_name='br_fri', to='dishapp.dish', verbose_name='Блюдо завтрак пт')),
                ('br_mon', models.ForeignKey(help_text='Блюдо завтрак пн', on_delete=django.db.models.deletion.CASCADE, related_name='br_mon', to='dishapp.dish', verbose_name='Блюдо завтрак пн')),
                ('br_sat', models.ForeignKey(help_text='Блюдо завтрак сб', on_delete=django.db.models.deletion.CASCADE, related_name='br_sat', to='dishapp.dish', verbose_name='Блюдо завтрак сб')),
                ('br_sun', models.ForeignKey(help_text='Блюдо завтрак вс', on_delete=django.db.models.deletion.CASCADE, related_name='br_sun', to='dishapp.dish', verbose_name='Блюдо завтрак вс')),
                ('br_thu', models.ForeignKey(help_text='Блюдо завтрак чт', on_delete=django.db.models.deletion.CASCADE, related_name='br_thu', to='dishapp.dish', verbose_name='Блюдо завтрак чт')),
                ('br_tue', models.ForeignKey(help_text='Блюдо завтрак вт', on_delete=django.db.models.deletion.CASCADE, related_name='br_tue', to='dishapp.dish', verbose_name='Блюдо завтрак вт')),
                ('br_wed', models.ForeignKey(help_text='Блюдо завтрак ср', on_delete=django.db.models.deletion.CASCADE, related_name='br_wed', to='dishapp.dish', verbose_name='Блюдо завтрак ср')),
                ('dn_fri', models.ForeignKey(help_text='Блюдо ужин пт', on_delete=django.db.models.deletion.CASCADE, related_name='dn_fri', to='dishapp.dish', verbose_name='Блюдо ужин пт')),
                ('dn_mon', models.ForeignKey(help_text='Блюдо ужин пн', on_delete=django.db.models.deletion.CASCADE, related_name='dn_mon', to='dishapp.dish', verbose_name='Блюдо ужин пн')),
                ('dn_sat', models.ForeignKey(help_text='Блюдо ужин сб', on_delete=django.db.models.deletion.CASCADE, related_name='dn_sat', to='dishapp.dish', verbose_name='Блюдо ужин сб')),
                ('dn_sun', models.ForeignKey(help_text='Блюдо ужин вс', on_delete=django.db.models.deletion.CASCADE, related_name='dn_sun', to='dishapp.dish', verbose_name='Блюдо ужин вс')),
                ('dn_thu', models.ForeignKey(help_text='Блюдо ужин чт', on_delete=django.db.models.deletion.CASCADE, related_name='dn_thu', to='dishapp.dish', verbose_name='Блюдо ужин чт')),
                ('dn_tue', models.ForeignKey(help_text='Блюдо ужин вт', on_delete=django.db.models.deletion.CASCADE, related_name='dn_tue', to='dishapp.dish', verbose_name='Блюдо ужин вт')),
                ('dn_wed', models.ForeignKey(help_text='Блюдо ужин ср', on_delete=django.db.models.deletion.CASCADE, related_name='dn_wed', to='dishapp.dish', verbose_name='Блюдо ужин ср')),
                ('lu_fri', models.ForeignKey(help_text='Блюдо обед пт', on_delete=django.db.models.deletion.CASCADE, related_name='lu_fri', to='dishapp.dish', verbose_name='Блюдо обед пт')),
                ('lu_mon', models.ForeignKey(help_text='Блюдо обед пн', on_delete=django.db.models.deletion.CASCADE, related_name='lu_mon', to='dishapp.dish', verbose_name='Блюдо обед пн')),
                ('lu_sat', models.ForeignKey(help_text='Блюдо обед сб', on_delete=django.db.models.deletion.CASCADE, related_name='lu_sat', to='dishapp.dish', verbose_name='Блюдо обед сб')),
                ('lu_sun', models.ForeignKey(help_text='Блюдо обед вс', on_delete=django.db.models.deletion.CASCADE, related_name='lu_sun', to='dishapp.dish', verbose_name='Блюдо обед вс')),
                ('lu_thu', models.ForeignKey(help_text='Блюдо обед чт', on_delete=django.db.models.deletion.CASCADE, related_name='lu_thu', to='dishapp.dish', verbose_name='Блюдо обед чт')),
                ('lu_tue', models.ForeignKey(help_text='Блюдо обед вт', on_delete=django.db.models.deletion.CASCADE, related_name='lu_tue', to='dishapp.dish', verbose_name='Блюдо обед вт')),
                ('lu_wed', models.ForeignKey(help_text='Блюдо обед ср', on_delete=django.db.models.deletion.CASCADE, related_name='lu_wed', to='dishapp.dish', verbose_name='Блюдо обед ср')),
            ],
        ),
    ]
