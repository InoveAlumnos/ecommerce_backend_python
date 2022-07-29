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
    list_display = ('user', 'comic', 'favorite', 'cart')
    list_display_links = ('user', 'comic')
    list_filter= ('favorite','cart')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")
    list_display_links = ("user", "phone")
    list_filter = ("user", "phone")