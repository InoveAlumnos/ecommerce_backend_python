#!/usr/bin/env python

from applications.ecommerce.auth.serializers import LoginSerializer
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
                    try:
                        token = Token.objects.get(user=account)

                    except Token.DoesNotExist:
                        # En caso de token inexistente, lo creamos automáticamente
                        token = Token.objects.create(user=account)

                    # Devolvemos la respuesta personalizada
                    return Response(status=200, data={"username": username, "token": token.key})

                else:
                    print(request.data)
                    # Si las credenciales son invalidas, devolvemos mensaje de error:
                    return Response(status=401, data={"response": "Error", "error_message": "Unauthorized - Credenciales invalidas"})

            return Response(status = 400, data = {"Error": "Bad Request", "error_message": f"{serializer.errors}"})

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"Error": "Internal server error", "description": e})