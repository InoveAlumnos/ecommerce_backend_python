#!/usr/bin/env python

from applications.ecommerce.models import Comic, WishList
from django.contrib.auth.models import User
from rest_framework import serializers


class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('__all__')


class WishListSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(write_only = True, queryset = User.objects.all())
    comic_id = serializers.PrimaryKeyRelatedField(write_only = True, queryset = Comic.objects.all())

    class Meta:
        model = WishList
        fields = ('__all__')
