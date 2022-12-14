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

comic_responses = {
    "200": openapi.Response(
        description='Operación exitosa',
        examples = {
            "application/json": {
                "id": 0,
                "marvel_id": 10,
                "title": "string",
                "description": "string",
                "price": 0,
                "stock_qty": 10,
                "picture": "string",
                "stars": 5
            }
        }
    ),

    "400": openapi.Response(
        description='Bad Request - Faltan parámetros en el request',
        examples={
            "application/json": {
                'error': 'Bad Request',
                'detail': 'No se enviaron los parámetros necesarios'
            }
        }
    ),

    "403": openapi.Response(
        description='Forbidden',
        examples={
            "application/json": {
                'error': 'Forbidden',
                'detail': 'Usted no tiene permiso para realizar esta acción.'
            }
        }
    ),
    
    "500": openapi.Response(
        description='Internal Server Error',
        examples={
            "application/json": {
                'error': 'Internal Server Error',
                'detail': 'Ocurrió un error en el servidor'
            }
        }
    ),
}

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
            return Comic.objects.all()[int(offset):int(offset) + int(limit)]
        return Comic.objects.all()

    limit = openapi.Parameter('limit', openapi.IN_QUERY,
                        description="Límite de resultados a mostrar",
                        type=openapi.TYPE_INTEGER)

    offset = openapi.Parameter('offset', openapi.IN_QUERY,
                description="Número de resultados a omitir",
                type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(tags = ["Comics y Wishlists"], responses = comic_responses, manual_parameters = [limit, offset])

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class PostComicAPIView(CreateAPIView):
    __doc__ = """
    PostComicAPIView \n

    **Vista de API para administradores** \n

    Vista de API genérica que recibe peticiones de tipo POST para hacer un insert en la base de datos. \n
    """

    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(auto_schema = None, tags = ["Administrador"], responses = comic_responses) 

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

  
class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = """
    ListCreateComicAPIView \n

    **Vista de API para administradores** \n

    Vista de API genérica que recibe de peticiones GET y POST. \n

    El método GET devuelve una lista de todos los comics presentes en la base de datos. \n
    
    El método POST recibe una lista de comics y permite hacer un insert en la base de datos. \n

    **Importante: el método post sólo puede ser utilizado por administradores de la aplicación.** \n
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(auto_schema = None, tags = ["Administrador"], responses = comic_responses)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema = None, tags = ["Administrador"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = """
    RetrieveUpdateComicAPIView \n

    **Vista de API para administradores** \n

    Vista de API genérica que recibe peticiones de tipo GET, PUT y PATCH. Permite actualizar un registro u obtenerlo. \n
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    
    @swagger_auto_schema(auto_schema = None, tags = ["Administrador"], responses = comic_responses)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema = None, tags = ["Administrador"], responses = comic_responses)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema = None, tags = ["Administrador"], responses = comic_responses)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class DestroyComicAPIView(DestroyAPIView):
    __doc__ = """
    DestroyComicAPIView \n

    **Vista de API para administradores** \n

    Vista de API genérica que permite eliminar comics de la base de datos. \n
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(auto_schema = None, tags = ["Administrador"], responses = comic_responses)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
