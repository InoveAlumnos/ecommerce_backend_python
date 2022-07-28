#!/usr/bin/env python

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class LoginUserAPIView(APIView):
    '''
    @NAME: LoginUserAPIView

    @DESC: Vista de API personalizada para recibir peticiones de tipo POST para Login de usuarios.
    
    @ROUTE: /user/login

    @METHODS: POST

    @HEADERS: 
        - Content-Type: application/json

    @PAYLOAD: 
        - username: str
        - password: str

    @RETURN:
        - username: str
        - token: str
    '''

    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []

    def post(self, request, format = None):

        try:
            username = request.data.get('username')
            password = request.data.get('password')
            account = authenticate(username=username, password=password)

            # Si el usuario existe y sus credenciales son validas, intentamos obtener el token
            if account:
                try:
                    token = Token.objects.get(user=account)

                except Token.DoesNotExist:
                    # En caso de token inexistente, lo creamos automáticamente
                    token = Token.objects.create(user=account)

                # Devolvemos la respuesta personalizada
                return Response(status = 200, data = {"username": username, "token": token.key})

            else:
                # Si las credenciales son invalidas, devolvemos mensaje de error:
                return Response(status = 401, data = {"response": "Error", "error_message": "Unauthorized - Credenciales invalidas"})

        except Exception as exception:
            print(exception)

            # Si aparece alguna excepción, devolvemos un mensaje de error
            return Response(status = 500, data = {"response": "Error", "error_message": "Internal server error"})
