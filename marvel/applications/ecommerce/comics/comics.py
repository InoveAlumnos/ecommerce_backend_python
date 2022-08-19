#!/usr/bin/env python

'''
APIs genéricas para realizar un CRUD a la base de datos - Tabla Comic
'''

from applications.ecommerce.models import Comic
from applications.ecommerce.comics.serializers import *
from rest_framework.permissions import IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class GetComicAPIView(ListAPIView):
    __doc__ = """
    GetComicAPIView \n

    Vista de API genérica que recibe peticiones de tipo GET y devuelve una lista de todos los comics presentes en la base de datos. \n
    
    Se pueden enviar en URL los parámetros limit y offset. **?limit=n&offset=m** \n
    """

    serializer_class = ComicSerializer
    permission_classes = [HasAPIKey]
    authentication_classes = []

    def get_queryset(self):
        limit = self.request.GET.get("limit", 20)
        offset = self.request.GET.get("offset", 0)
        if limit is not None:
            return Comic.objects.all()[int(offset):int(limit)]
        return Comic.objects.all()


class PostComicAPIView(CreateAPIView):
    __doc__ = """
    PostComicAPIView \n

    Vista de API genérica que recibe peticiones de tipo POST para hacer un insert en la base de datos. \n
    """

    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

  
class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = """
    ListCreateComicAPIView \n

    Vista de API genérica que recibe de peticiones GET y POST. \n

    El método GET devuelve una lista de todos los comics presentes en la base de datos. \n
    
    El método POST recibe una lista de comics y permite hacer un insert en la base de datos. \n

    **Importante: el método post sólo puede ser utilizado por administradores de la aplicación.** \n
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = """
    RetrieveUpdateComicAPIView \n

    Vista de API genérica que recibe peticiones de tipo GET, PUT y PATCH. Permite actualizar un registro u obtenerlo. \n
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class DestroyComicAPIView(DestroyAPIView):
    __doc__ = """
    DestroyComicAPIView \n

    Vista de API genérica que permite eliminar comics de la base de datos. \n
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]