#!/usr/bin/env python

from applications.ecommerce.models import Profile
from applications.ecommerce.permissions import IsClient
from applications.ecommerce.auth.serializers import ProfileDataSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class UpdateProfileAPIView(APIView):

    serializer_class = [ProfileDataSerializer]
    parser_classes = [JSONParser]
    permission_classes = [IsClient]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        try:
            # TODO: Validar que el token y el usuario coinciden
            # Validate that the token and the user coincide
            if not dict(request.headers).get("User-Agent"):
                return Response(status=401, data={"error": "UnAuthorized", "error_message": "No se ha enviado el header 'user-agent'"})

            consumer = User.objects.get(username = request.data.get("username"))
            
            if not Token.objects.get(key = request.headers.get("user-agent").split(" ")[1]).user == consumer:
                return Response(status=401, data = {"error": "La sesión y el usuario no coinciden"})

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
