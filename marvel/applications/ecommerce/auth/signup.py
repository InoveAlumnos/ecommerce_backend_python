#!/usr/bin/env python

from applications.ecommerce.models import Profile
from applications.ecommerce.groups import ClientGroup
from applications.ecommerce.permissions import IsClient
from applications.ecommerce.auth.serializers import RegisterSerializer
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated   
from rest_framework.authentication import TokenAuthentication

        
class SignUpClientAPIView(APIView):

    serializer_class = RegisterSerializer
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data = request.data)

            if serializer.is_valid():
                
                try:
                    user = serializer.save()

                except IntegrityError:
                    return Response(status = 400, data = {"error": f"El nombre de usuario {request.data['username']} no está disponible"})

                except Exception as e:                    
                    return Response(status = 500, data = {"error": "Internal server error", "description": e})
                
                ClientGroup().agregar_usuario(user)
                return Response(status = 200, data = serializer.data)
            
            return Response(status = 400, data = {"error": "Bad Request", "error_message": f"{serializer.errors}"})

        except Exception as e:
            return Response(status = 500, data = {"error": "Internal server error", "description": e})


class SignUpUserAPIView(SignUpClientAPIView):
    '''
    @NAME: SignUpUserAPIView \n

    @DESC: Vista de API personalizada para recibir peticiones de tipo POST para Registro de usuarios. \n
    
    @ROUTE: /user/signup/ \n

    @METHODS: POST \n

    @HEADERS: \n
        - Content-Type: application/json \n
        - ApiKey: <API_KEY> \n

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

    permission_classes = [IsAuthenticated, IsClient]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            serializer = super().serializer_class(data = request.data)

            if serializer.is_valid():
                try:
                    user = serializer.save()

                except IntegrityError:
                    return Response(status = 400, data = {"error": f"El nombre de usuario {request.data['username']} no está disponible"})

                except:                    
                    return Response(status = 500, data = {"error": "Internal server error", "description": e})
                
                # NOTE: Creo perfil usando un filtrado del request, en caso de que luego se agreguen mas campos, va a ser mas facil
                profile = Profile(user = user, **{key: dict(request.data).get(key, "Desconocido")
                                for key in dict(request.data) if key in ['phone', "address", "province_state", "country", "postal_code"]})
                profile.save()

                return Response(status = 200, data = serializer.data)
            
            return Response(status = 400, data = {"Error": "Bad Request", "error_message": "No se enviaron los valores necesarios"})

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"Error": "Bad Request", "error_message": "Ocurrío un error en el servidor", "description": e})
