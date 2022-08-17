#!/usr/bin/env python

from applications.ecommerce.models import Profile
from applications.ecommerce.groups import ClientGroup, ConsumerGroup
from applications.ecommerce.auth.serializers import RegisterSerializer
from django.db.utils import IntegrityError
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
        

class SignUpClientAPIView(APIView):
    __doc__ = """
    SignUpUserAPIView \n

    Vista de API personalizada para recibir peticiones de tipo POST para Registro de Clientes. \n
    """

    serializer_class = RegisterSerializer
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties = {
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format = openapi.FORMAT_PASSWORD, description='password'),
            }
        ),
    responses = {
        "200": openapi.Response(
            description='Registro exitoso',
            examples = {
                "application/json": {
                    "user_id": 1,
                    "username": "username",
                    "first_name": "first_name",
                    "last_name": "last_name",
                    "email": "info@inove.com.ar",
                }
            }
        ),

        "400": openapi.Response(
            description='Bad Request',
            examples={
                "application/json": {
                    'error': 'Bad Request',
                    'message': 'No se enviaron los parámetros necesarios'
                }
            }
        ),
        
        "403": openapi.Response(
            description='Unavailable',
            examples={
                "application/json": {
                    'error': 'Unavailable',
                    'message': 'El nombre de usuario no está disponible'
                }
            }
        ),
        "500": openapi.Response(
            description='Internal Server Error',
            examples={
                "application/json": {
                    'error': 'Internal Server Error',
                    'message': 'Ocurrió un error en el servidor'
                }
            }
        ),
    }
    )
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data = request.data)

            if serializer.is_valid():
                
                try:
                    user = serializer.save()
                    # Agregar al usuario al grupo "client"
                    ClientGroup().agregar_usuario(user)

                except IntegrityError:
                    return Response(status = 400, data = {"error": "Unavailable", "message": f"El nombre de usuario {request.data['username']} no está disponible"})

                except Exception as e:                    
                    return Response(status = 500, data = {"error": "Internal server error", "description": e})
                
                return Response(status = 200, data = serializer.data)
            
            return Response(status = 400, data = {"error": "Bad Request", "message": f"Los siguientes campos son obligatorios: {list(serializer.errors.keys())}"})

        except Exception as e:
            return Response(status = 500, data = {"error": "Internal server error", "description": e})


class SignUpUserAPIView(APIView):
    __doc__ = """
    SignUpUserAPIView \n

    Vista de API personalizada para recibir peticiones de tipo POST para Registro de usuarios. \n

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key**. \n
    """

    serializer_class = RegisterSerializer
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties = {
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format = openapi.FORMAT_PASSWORD, description='password'),
        }
    ),
    responses = {
        "200": openapi.Response(
            description='Registro exitoso',
            examples = {
                "application/json": {
                    "user_id": 1,
                    "username": "username",
                    "first_name": "first_name",
                    "last_name": "last_name",
                    "email": "info@inove.com.ar",
                }
            }
        ),

        "400": openapi.Response(
            description='Bad Request',
            examples={
                "application/json": {
                    'error': 'Bad Request',
                    'message': 'No se enviaron los parámetros necesarios'
                }
            }
        ),

        "403": openapi.Response(
            description='Unavailable',
            examples={
                "application/json": {
                    'error': 'Unavailable',
                    'message': 'El nombre de usuario no está disponible'
                }
            }
        ),
        
        "500": openapi.Response(
            description='Internal Server Error',
            examples={
                "application/json": {
                    'error': 'Internal Server Error',
                    'message': 'Ocurrió un error en el servidor'
                }
            }
        ),
    }
    )

    def post(self, request, *args, **kwargs):

        try:
            serializer = self.serializer_class(data = request.data)

            if serializer.is_valid():
                try:
                    user = serializer.save()
                    ConsumerGroup().agregar_usuario(user)

                except IntegrityError as ie:
                    print(ie)
                    return Response(status = 403, data = {"error": "unavailable", "message": f"El nombre de usuario {request.data['username']} no está disponible"})

                except Exception as e:
                    print(e)                    
                    return Response(status = 500, data = {"error": "Internal server error", "message": "Ocurrió un error en el servidor"})
                
                # NOTE: Creo perfil usando un filtrado del request, en caso de que luego se agreguen mas campos, va a ser mas facil
                profile = Profile(user = user, **{key: dict(request.data).get(key, "Desconocido")
                                for key in dict(request.data) if key in ['phone', "address", "province_state", "country", "postal_code"]})
                profile.save()

                return Response(status = 200, data = serializer.data)

            return Response(status = 400, data = {"error": "Bad Request", "message": f"Los siguientes campos son obligatorios: {list(serializer.errors.keys())}"})

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"error": "Internal server error", "message": "Ocurrió un error en el servidor"})
