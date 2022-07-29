# Generated by Django 3.2.2 on 2022-07-29 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='', max_length=120, verbose_name='first_name')),
                ('last_name', models.CharField(default='', max_length=120, verbose_name='last_name')),
                ('email', models.EmailField(default='', max_length=254, verbose_name='email')),
                ('phone', models.CharField(default='', max_length=120, verbose_name='phone')),
                ('user', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'db_table': 'E Commerce UserData',
            },
        ),
    ]