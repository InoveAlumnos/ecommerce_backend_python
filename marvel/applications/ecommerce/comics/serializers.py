#!/usr/bin/env python

from yaml import serialize
from applications.ecommerce.models import Comic, WishList
from django.contrib.auth.models import User
from rest_framework import serializers


class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('__all__')


class WishListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(write_only = True, queryset = User.objects.all())
    comic = serializers.PrimaryKeyRelatedField(write_only = True, queryset = Comic.objects.all())

    class Meta:
        model = WishList
        fields = ('__all__')


class WishListQuerySerializer(serializers.Serializer):
    on_cart = serializers.IntegerField(required = False)
    on_cart = serializers.IntegerField(required = False)
