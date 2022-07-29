#!/usr/bin/env python

from django.contrib import admin
from applications.ecommerce.models import *


@admin.register(Comic)
class ComicsAdmin(admin.ModelAdmin):
    # NOTE: Para seleccionar los campos en la tabla de registros
    list_display = ('marvel_id', 'title', 'stock_qty', 'price')

    # NOTE: Filtro lateral de elementos:
    list_filter= ('marvel_id','title')
    
    # NOTE: Buscador de elementos en la columna:
    search_fields = ['title']

    # NOTE: Genera un campo desplegable con los registros seleccionados.
    fieldsets = (
        (None, {
            'fields': ('marvel_id', 'title', 'stock_qty')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('description','price', 'picture'),
        }),
    )


@admin.register(WishList)
class wish_listAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'comic_id', 'favorite', 'cart')
    list_display_links = ('user_id', 'comic_id')
    list_filter= ('favorite','cart')