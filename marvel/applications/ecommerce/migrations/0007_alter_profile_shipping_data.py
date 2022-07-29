# Generated by Django 3.2.2 on 2022-07-29 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_alter_profile_shipping_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='shipping_data',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='ecommerce.shippingdata', verbose_name='Shipping Data'),
        ),
    ]
