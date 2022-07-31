#!/usr/bin/env python

'''
APIs genéricas para realizar un CRUD a la base de datos - Tabla Comic y WishList
'''

from applications.ecommerce.models import Comic,WishList
from applications.ecommerce.comics.serializers import ComicSerializer, WishListSerializer
from rest_framework_api_key.permissions import HasAPIKey
from applications.ecommerce.permissions import IsClient
from django.contrib.auth.models import User
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
    __doc__ = f'''
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''

    serializer_class = ComicSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        limit = self.request.query_params.get('limit', 20)
        offset = self.request.query_params.get('offset', 0)
        if limit is not None:
            return Comic.objects.all()[int(offset):int(limit)]
        return Comic.objects.all()


class PostComicAPIView(CreateAPIView):
    __doc__ = f'''
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]

  
class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = f'''
    `[METODO GET-POST]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    Tambien nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]


class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''
    `[METODO GET-PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro, o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]


class DestroyComicAPIView(DestroyAPIView):
    __doc__ = f'''
    `[METODO DELETE]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]



class GetWishListAPIView(ListAPIView):
    __doc__ = f'''
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todas las wishlists presentes en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsClient]


class GetWishListByUserAPIView(ListAPIView):
    __doc__ = f'''
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todas las wishlists presentes en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        user = User.objects.get(id=uid)
        comments = WishList.objects.filter(user=user)
        return comments


class PostWishListAPIView(CreateAPIView):
    __doc__ = f'''
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = []
