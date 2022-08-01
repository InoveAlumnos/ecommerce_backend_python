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


class LoginClientAPIView(APIView):
    '''
    @NAME: LoginClientAPIView

    @DESC: Vista de API personalizada para recibir peticiones de tipo POST para Login de clientes.
    
    @ROUTE: /client/login

    @METHODS: POST

    @HEADERS: 
        - Content-Type: application/json

    @PAYLOAD: 
        - username: str
        - password: str

    @RETURN:
        - username: str
        - api-key: str
    '''

    serializer_class = LoginSerializer
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []

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
                        # Crear una apikey para el usuario. # TODO: Agregarle fecha de expiración 
                        _, key = APIKey.objects.create_key(name = username)
                        
                        return Response(status = 200, data = {'username': username, 'api-key': key})
                    
                    else:
                        return Response(status = 401, data = {"error": "Unauthorized", "error_message": "Tu usuario no pertenece al grupo cliente"})

                else:
                    print("Autenticación fallida:", request.data)
                    # Si las credenciales son invalidas, devolvemos mensaje de error:
                    return Response(status = 401, data = {"error": "Unauthorized", "error_message": "Credenciales invalidas"})

            return Response(status = 400, data = {"error": "Bad Request", "error_message": f"{serializer.errors}"})

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"error": "Internal server error", "description": e})


class LoginUserAPIView(APIView):
    '''
    @NAME: LoginUserAPIView

    @DESC: Vista de API personalizada para recibir peticiones de tipo POST para Login de usuarios.
    
    @ROUTE: /user/login

    @METHODS: POST

    @HEADERS: 
        - Content-Type: application/json
        - X-Api-Key: <api-key>

    @PAYLOAD: 
        - username: str
        - password: str

    @RETURN:
        - username: str
        - token: str
    '''

    serializer_class = LoginSerializer
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = [HasAPIKey]

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

                    except Token.DoesNotExist:
                        # En caso de token inexistente, lo creamos
                        token = Token.objects.create(user=account)

                        return Response(status = 200, data = {'username': username, 'token': token.key})

                    else:
                        return Response(status = 401, data = {'error': 'Unauthorized', "error_message": "Credenciales inválidas"})
                
                else:
                    print("Autenticación fallida:", request.data)
                    # Si las credenciales son invalidas, devolvemos mensaje de error:
                    return Response(status=401, data={"error": "Unauthorized", "error_message": "Credenciales invalidas"})

            return Response(status = 400, data = {"error": "Bad Request", "error_message": f"{serializer.errors}"})

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"error": "Internal server error", "description": e})
