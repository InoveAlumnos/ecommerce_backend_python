#!/usr/bin/env python

from applications.ecommerce.auth.serializers import ChangePasswordSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated   
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class ResetPasswordView(UpdateAPIView):
    '''
    @NAME: ResetPasswordView \n

    @DESCRIPTION: Cambiar/Resetear contraseña de un usuario - **NO** aplica a usuarios que hayan olvidado su contraseña,
                  está pensado para usuarios **logueados** que desean cambiar su contraseña \n
    '''

    serializer_class = ChangePasswordSerializer
    parser_classes = [JSONParser]
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties = {
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='old_password'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='new_password'),
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
                    'message': 'No se enviaron los parámetros necesarios'
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
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            
            # Verificar que la contraseña actual sea correcta
            print("Username", request.data.get("username"))
            print("Password", request.data.get("old_password"))
            account = authenticate(username = request.data.get("username"), password = request.data.get("old_password"))

            if account:
                # Cambiar contraseña
                user = User.objects.get(username = request.data.get("username"))

                # Si es un usuario de grupo test - omitir cambio de contraseña
                if user.groups.filter(name = "test").exists():
                    return Response(status = 200, data = {"success": f"Se actualizó la contraseña de {user.username} satisfactoriamente"})

                user.set_password(request.data.get("new_password"))
                user.save()

                return Response(status = 200, data = {"success": f"Se actualizó la contraseña de {user.username} satisfactoriamente"})
            
            return Response({"old_password": ["Wrong password."]}, status = 401)

        return Response(status = 400, data = {"Error": "Bad Request", "error_message": f"{serializer.errors}"})
