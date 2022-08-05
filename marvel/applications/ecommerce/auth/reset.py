#!/usr/bin/env python

from applications.ecommerce.auth.serializers import ChangePasswordSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated   
from rest_framework.authentication import TokenAuthentication


class ResetPasswordView(UpdateAPIView):
    '''
    @NAME: ResetPasswordView \n

    @DESCRIPTION: Cambiar/Resetear contraseña de un usuario - **NO** aplica a usuarios que hayan olvidado su contraseña,
                  está pensado para usuarios **logueados** que desean cambiar su contraseña \n

    @ROUTE: /user/reset-password/ \n

    @METHODS: PATCH \n

    @HEADERS: \n
        - Content-Type: application/json \n
        - Authorization: Token <token> \n

    @PAYLOAD: \n
        - username: str \n
        - old_password: str \n
        - new_password: str \n
    '''

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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
