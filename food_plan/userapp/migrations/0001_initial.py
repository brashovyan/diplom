# Generated by Django 4.2.7 on 2023-12-06 17:28

from django.db import migrations, models
import django.utils.timezone
import userapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('height', models.FloatField(help_text='Введите ваш рост в сантиметрах', verbose_name='Рост (см)')),
                ('weight', models.FloatField(help_text='Введите ваш вес в килограммах', verbose_name='Вес (кг)')),
                ('date_of_birth', models.DateField(help_text='Введите вашу дату рождения', verbose_name='Дата рождения')),
                ('sex', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], help_text='Выберите пол', max_length=1, verbose_name='Пол')),
                ('image', models.ImageField(blank=True, help_text='Выберите фото профиля', null=True, upload_to='user/', verbose_name='Фото')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', userapp.models.CustomUserManager()),
            ],
        ),
    ]