#!/usr/bin/env python

from applications.ecommerce.auth.serializers import LoginSerializer
from applications.ecommerce.groups import ClientGroup
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework_api_key.models import APIKey
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class LoginClientAPIView(APIView):
    __doc__ = """
    LoginClientAPIView \n

    Vista de API personalizada para recibir peticiones de tipo POST para Login de clientes. \n
    """

    serializer_class = LoginSerializer
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []


    @swagger_auto_schema(
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties = {
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
            }
        ),
    responses = {
        "200": openapi.Response(
            description='Registro exitoso',
            examples = {
                "application/json": {
                    "username": "username",
                    "api-key": "hlvQaIRo.1lrb7dV69yjb07vhRLsE7wrCHNOmwsav",
                }
            }
        ),

        "400": openapi.Response(
            description='Bad Request',
            examples={
                "application/json": {
                    'error': 'Bad Request',
                    'detail': 'No se enviaron los parámetros necesarios'
                }
            }
        ),

        "401": openapi.Response(
            description='Unauthorized',
            examples={
                "application/json": {
                    'error': 'Unauthorized',
                    'detail': 'Credenciales inválidas'
                }
            }
        ),

        "500": openapi.Response(
            description='Internal Server Error',
            examples={
                "application/json": {
                    'error': 'Internal Server Error',
                    'detail': 'Ocurrió un error en el servidor'
                }
            }
        ),
    }
    )


    def post(self, request, *args, **kwargs):

        try:
            serializer = self.serializer_class(data = request.data)

            if serializer.is_valid():

                username = request.data.get('username')
                password = request.data.get('password')
                account = authenticate(username = username, password = password)

                # Si el usuario existe y sus credenciales son validas, intentamos obtener el token
                if account:
                    # Devolvemos Api-Key para cliente
                    if account.groups.filter(name = ClientGroup.group.name).exists():

                        # Crear una apikey para el usuario.
                        _, key = APIKey.objects.create_key(name = username)
                        user = User.objects.get(username = username)
                        return Response(status = 200, data = {'username': username, 'uid': user.id, 'api-key': key})
                    
                    else:
                        return Response(status = 403, data = {"error": "Unauthorized", "detail": "Tu usuario no tiene los permisos para realizar esta acción"})

                else:
                    print("Autenticación fallida:", request.data)
                    # Si las credenciales son invalidas, devolvemos mensaje de error:
                    return Response(status = 401, data = {"error": "Unauthorized", "detail": "Credenciales invalidas"})

            return Response(status = 400, data = {"error": "Bad Request", "detail": f"Los siguientes campos son obligatorios: {list(serializer.errors.keys())}"})

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"error": "Internal server error", "description": e})


class LoginUserAPIView(APIView):
    __doc__ = """
    LoginUserAPIView \n

    Vista de API personalizada para recibir peticiones de tipo POST para Login de usuarios. \n

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key**. \n
    """

    serializer_class = LoginSerializer
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = [HasAPIKey]


    @swagger_auto_schema(
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties = {
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
            }
        ),
    responses = {
        "200": openapi.Response(
            description='Registro exitoso',
            examples = {
                "application/json": {
                    "username": "username",
                    "api-key": "hlvQaIRo.1lrb7dV69yjb07vhRLsE7wrCHNOmwsav",
                }
            }
        ),

        "400": openapi.Response(
            description='Bad Request - Faltan parámetros en el request',
            examples={
                "application/json": {
                    'error': 'Bad Request',
                    'detail': 'No se enviaron los parámetros necesarios'
                }
            }
        ),

        "401": openapi.Response(
            description='Unauthorized - No matchean usuario y contraseña',
            examples={
                "application/json": {
                    'error': 'Unauthorized',
                    'detail': 'Credenciales inválidas'
                }
            }
        ),

        "403": openapi.Response(
            description='Forbidden - Falta API Key',
            examples={
                "application/json": {
                    'error': 'Forbidden',
                    'detail': 'Usted no tiene permiso para realizar esta acción.'
                }
            }
        ),
        
        "500": openapi.Response(
            description='Internal Server Error',
            examples={
                "application/json": {
                    'error': 'Internal Server Error',
                    'detail': 'Ocurrió un error en el servidor'
                }
            }
        ),
    }
    )


    def post(self, request, *args, **kwargs):
            
        try:
            serializer = self.serializer_class(data = request.data)

            if serializer.is_valid():

                username = request.data.get('username')
                password = request.data.get('password')
                account = authenticate(username = username, password = password)
                # Si el usuario existe y sus credenciales son validas, intentamos obtener el token
                if account:

                    try:
                        token = Token.objects.get(user=account)
                        user = User.objects.get(username = username)

                    except Token.DoesNotExist:
                        # En caso de token inexistente, lo creamos
                        token = Token.objects.create(user=account)
                        
                        return Response(status = 200, data = {'username': username, 'uid': user.id, 'token': token.key})

                    else:
                        return Response(status = 200, data = {'username': username, 'uid': user.id, 'token': token.key})

                else:
                    print("Autenticación fallida:", request.data)
                    # Si las credenciales son invalidas, devolvemos mensaje de error:
                    return Response(status=401, data = {"error": "Unauthorized", "detail": "Credenciales invalidas"})

            return Response(status = 400, data = {"error": "Bad Request", "detail": f"Los siguientes campos son obligatorios: {list(serializer.errors.keys())}"})

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"error": "Internal server error"})
