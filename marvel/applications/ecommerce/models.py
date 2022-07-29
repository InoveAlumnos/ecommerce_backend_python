#!/usr/bin/env python

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Comic(models.Model):
    id = models.BigAutoField(db_column = 'ID', primary_key = True)

    marvel_id = models.PositiveIntegerField(
        verbose_name='marvel ids', default = 1, unique=True)

    title = models.CharField(verbose_name = 'titles', max_length = 120, default = '')

    description = models.TextField(verbose_name = 'descriptions', default = '')

    price = models.FloatField(verbose_name = 'prices',
                              max_length = 5, default = 0.00)

    stock_qty = models.PositiveIntegerField(
        verbose_name = 'stock qty', default = 0)

    picture = models.URLField(verbose_name = 'pictures', default = '')

    class Meta:
        db_table = 'E Commerce Comic'

    def __str__(self):
        return f'Comic: ID: {self.id} - Nombre: {self.title} - Precio: {self.price} - Cantidad: {self.stock_qty}'


class WishList(models.Model):
    id = models.BigAutoField(db_column = 'ID', primary_key = True)

    user = models.ForeignKey(
        User, verbose_name = 'User', on_delete = models.DO_NOTHING, default = 1, blank = True)

    comic = models.ForeignKey(
        Comic, verbose_name = 'Comic', on_delete = models.DO_NOTHING, default = 1, blank = True)

    favorite = models.BooleanField(verbose_name = 'Faved', default = None)

    cart = models.BooleanField(verbose_name = 'On Cart', default = None)

    wished_qty = models.PositiveIntegerField(
        verbose_name = 'wished_qty', default = 0)

    bought_qty = models.PositiveIntegerField(
        verbose_name = 'buied_qty', default = 0)

    class Meta:
        db_table = 'E Commerce Wishlist'

    def __str__(self):
        return f'Wishlist: ID: {self.id} - User ID: {self.user} - Comic ID: {self.comic}'


class Profile(models.Model):
    id = models.BigAutoField(db_column = 'ID', primary_key = True)

    user = models.ForeignKey(
        User, verbose_name = 'User', on_delete = models.DO_NOTHING, default = 1, blank = True)

    phone = models.CharField(verbose_name = 'phone', max_length = 120, default = '')

    class Meta:
        db_table = 'E Commerce UserData'

    def __str__(self):
        return f'Profile: ID: {self.id} - User: {self.user} - Phone: {self.phone}'
