#!/usr/bin/env python

from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length = 128, min_length = 6, write_only = True
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

    def create(self, validated_data):
        return User.objects.create(**validated_data)

        
class SignUpUserAPIView(APIView):
    '''
    @NAME: SignUpUserAPIView \n

    @DESC: Vista de API personalizada para recibir peticiones de tipo POST para Registro de usuarios. \n
    
    @ROUTE: /user/signup/ \n

    @METHODS: POST \n

    @HEADERS: \n
        - Content-Type: application/json \n

    @PAYLOAD: \n 
        - username: str \n 
        - first_name: str \n
        - last_name: str \n
        - email: str \n
        - password: str \n

    @RETURN: usuario creado \n
        - username: str \n
        - first_name: str \n
        - last_name: str \n
        - email: str \n
    '''

    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser]

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status = 200, data = serializer.data)
        
        print(request.data)
        return Response(status = 400, data = {"Error": "Bad Request", "error_message": f"{serializer.errors}"})