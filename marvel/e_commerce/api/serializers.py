#!/usr/bin/env python

from e_commerce.models import Comic,WishList
from django.contrib.auth.models import User
from rest_framework import serializers

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('marvel_id','title', 'description', 'price', 'stock_qty', 'picture')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ("__all__")


class WishListSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(write_only=True,
                                                   queryset=User.objects.all())
    comic_id = serializers.PrimaryKeyRelatedField(write_only=True,
                                                   queryset=Comic.objects.all())
    
    class Meta:
        model = WishList
        fields = ('id','user_id','comic_id', 'favorite', 'cart', 'wished_qty', 'buied_qty')
