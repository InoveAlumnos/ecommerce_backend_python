#!/usr/bin/env python

from applications.ecommerce.models import Profile
from applications.ecommerce.permissions import IsClient
from applications.ecommerce.auth.serializers import ProfileDataSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UpdateProfileAPIView(APIView):
    __doc__ = """
    UpdateProfileAPIView \n

    Vista de API personalizada para recibir peticiones de tipo PATCH para actualizar el perfil de un cliente. \n

    No es necesario enviar todos los campos a actualizar, el único campo obligatorio es **username**, el resto son opcionales. \n
    
    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario
    a actualizar en el campo **Authorization**.\n
    """
    
    serializer_class = ProfileDataSerializer
    parser_classes = [JSONParser]
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    @swagger_auto_schema(
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties = {
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='phone'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='address'),
                'province_state': openapi.Schema(type=openapi.TYPE_STRING, description='province_state'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, description='country'),
                'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description='postal_code'),
            }
        ),
        
        responses = {
            "200": openapi.Response(
                description='Perfil actualizado correctamente',
                examples = {
                    "application/json": {
                        "message": "Perfil actualizado correctamente",
                    }
                }
            ),

            "400": openapi.Response(
                description='Bad Request',
                examples={
                    "application/json": {
                        'error': 'Bad Request',
                        'message': 'No se enviaron los parámetros necesarios o el usuario no existe'
                    }
                }
            ),

            "401": openapi.Response(
                description='Unauthorized',
                examples={
                    "application/json": {
                        'error': 'Unauthorized',
                        'message': 'Credenciales inválidas'
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

    def patch(self, request, *args, **kwargs):
        try:
            consumer = User.objects.get(username = request.data.get("username"))

            # Validar que el username coincide con el token enviado            
            if not Token.objects.get(key = request.headers.get("Authorization").split(" ")[1]).user == consumer:
                return Response(status=401, data = {"error": "Unauthorized", "message": "Credenciales inválidas - Token inválido"})

        except Exception as e:
            print(e)
            return Response(status=500, data = {"error": "Internal server error", "description": e})

        try:
            profile = Profile.objects.get(user = consumer)
        
        except IntegrityError:
            print("No se encontró el perfil del usuario")
            return Response(status = 400, data = {"error": f"El nombre de usuario {request.data['username']} es incorrecto"})

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"error": "Internal server error", "description": e})

        try:
            # Actualizar perfil
            [setattr(profile, key, value) for key, value in request.data.items() if key in profile.__dict__]
            profile.save()
        
        except Exception as e:
            print(e)
            return Response(status = 500, data = {"error": "Internal server error", "description": e})
        
        return Response(status = 200, data = {"message": "Perfil actualizado correctamente"})
