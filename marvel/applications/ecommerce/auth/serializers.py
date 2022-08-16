#!/usr/bin/env python

from rest_framework import serializers
from django.contrib.auth.models import User
from applications.ecommerce.models import Profile


class RegisterSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField( max_length = 128, min_length = 6, write_only = True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "password")


class ChangePasswordSerializer(serializers.Serializer):

    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "old_password", "new_password")
        

class ProfileDataSerializer(serializers.Serializer):

    username = serializers.CharField()

    class Meta:
        model = Profile
        fields = ("username",)
        