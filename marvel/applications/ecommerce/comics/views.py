#!/usr/bin/env python

'''
APIs genéricas para realizar un CRUD a la base de datos - Tabla Comic y WishList
'''

from django.db.utils import IntegrityError
from applications.ecommerce.models import Comic,WishList
from applications.ecommerce.comics.serializers import *
from applications.ecommerce.permissions import IsClient
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import (
    ListAPIView,  # (GET) Listar todos los elementos en la entidad  
    CreateAPIView,  # (POST) Inserta elementos 
    ListCreateAPIView,  # (GET-POST) Para leer e insertar elementos 
    RetrieveUpdateAPIView,  # (PUT) Recuperar y actualizar elementos
    DestroyAPIView  # (DELETE) Eliminar elementos de la base de datos
)


class GetComicAPIView(ListAPIView):
    __doc__ = """
    Vista de API genérica que recibe peticiones de tipo GET y devuelve una lista de todos los comics presentes en la base de datos. 
    Se pueden enviar en URL los parámetros limit y offset.
    """

    serializer_class = ComicSerializer
    permission_classes = [HasAPIKey]
    authentication_classes = []
    
    def get_queryset(self):
        limit = self.request.query_params.get('limit', 20)
        offset = self.request.query_params.get('offset', 0)
        if limit is not None:
            return Comic.objects.all()[int(offset):int(limit)]
        return Comic.objects.all()


class PostComicAPIView(CreateAPIView):
    __doc__ = """
    Vista de API genérica que recibe peticiones de tipo POST para hacer un insert en la base de datos.
    """

    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

  
class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = """
    Vista de API genérica que recibe de peticiones GET y POST.
    El método GET devuelve una lista de todos los comics presentes en la base de datos.
    El método POST recibe una lista de comics y permite hacer un insert en la base de datos.
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = """
    Vista de API genérica que recibe peticiones de tipo GET, PUT y PATCH. Permite actualizar un registro u obtenerlo.
    """

    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class DestroyComicAPIView(DestroyAPIView):
    __doc__ = """
    Vista de API genérica que permite eliminar comics de la base de datos.
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class GetWishListAPIView(ListAPIView):
    __doc__ = f'''
    `[METODO GET]`
    Vista de API genérica que devuelve una lista de todas las wishlists presentes en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class GetWishListByUsernameAPIView(ListAPIView):
    __doc__ = """
    Vista de API genérica que devuelve una lista de todas las wishlists presentes en la base de datos.
    """
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        username = self.kwargs.get("username")
        try:
            user = User.objects.get(username=username)
        
        except IntegrityError:
            print("No se pudo obtener el usuario")
            return Response(status = 400, data = {"error":f"No se encontró el usuario {username}"})
        
        comics = WishList.objects.filter(user=user)
        
        return comics


class GetWishListByUserIDAPIView(ListAPIView):
    __doc__ = """
    Vista de API genérica que devuelve una lista de todas las wishlists de un usuario.

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario
    a actualizar en el campo **Authorization**.\n
    """
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        uid = self.kwargs.get("uid")

        try:
            user = User.objects.get(id = uid)
        
        except IntegrityError:
            print("No se pudo obtener el usuario")
            raise Exception(f"No se encontró el usuario {uid}")
        
        comics = WishList.objects.filter(user=user)
        return comics


    def get(self, request, *args, **kwargs):
        # Validar que el username coincide con el token enviado
        uid = self.kwargs.get("uid")
        user = User.objects.get(id = uid)
        
        if not Token.objects.get(key = self.request.headers.get("Authorization").split(" ")[1]).user == user:
            return Response(status=401, data = {"error": "Unauthorized", "message": "Credenciales inválidas - Token inválido"})
        
        return super().get(request, *args, **kwargs)


class PostWishListAPIView(CreateAPIView):
    __doc__ = f'''
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # Validar que el username coincide con el token enviado
        if not Token.objects.get(key = request.headers.get("Authorization").split(" ")[1]).user == request.user:
            return Response(status=401, data = {"error": "Unauthorized", "message": "Credenciales inválidas - Token inválido"})

        return super().post(request, *args, **kwargs)