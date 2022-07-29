# Generated by Django 3.2.2 on 2022-07-29 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_alter_profile_shipping_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='shipping_data',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='profile',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='postal_code'),
        ),
        migrations.AddField(
            model_name='profile',
            name='province_state',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='province_state'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='phone'),
        ),
        migrations.DeleteModel(
            name='ShippingData',
        ),
    ]
