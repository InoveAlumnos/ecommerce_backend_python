#!/usr/bin/env python

'''
APIs genéricas para realizar un CRUD a la base de datos - Tabla Comic y WishList
'''

from applications.ecommerce.models import Comic,WishList
from applications.ecommerce.comics.serializers import ComicSerializer, WishListSerializer
from applications.ecommerce.permissions import IsClient
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import (
    ListAPIView,  # (GET) Listar todos los elementos en la entidad  
    CreateAPIView,  # (POST) Inserta elementos 
    ListCreateAPIView,  # (GET-POST) Para leer e insertar elementos 
    RetrieveUpdateAPIView,  # (PUT) Recuperar y actualizar elementos
    DestroyAPIView  # (DELETE) Eliminar elementos de la base de datos
)



mensaje_headder = '''
Ejemplo de header

headers = {
  'Authorization': 'Token 92937874f377a1ea17f7637ee07208622e5cb5e6',
  'actions': 'GET',
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=cfEuCX6qThpN6UC9eXypC71j6A4KJQagRSojPnqXfZjN5wJg09hXXQKCU8VflLDR'
}
'''


class GetComicAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsClient]
    authentication_classes = [TokenAuthentication]


class PostComicAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

  
class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-POST]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    Tambien nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro, o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DestroyComicAPIView(DestroyAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO DELETE]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]



class GetWishListAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los comics presentes en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PostWishListAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = []
