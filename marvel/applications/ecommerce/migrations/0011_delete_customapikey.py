# Generated by Django 3.2.2 on 2022-08-26 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_customapikey'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomAPIKey',
        ),
    ]