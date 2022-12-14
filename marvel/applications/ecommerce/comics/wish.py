#!/usr/bin/env python

"""
APIs genéricas para realizar un CRUD a la base de datos - Tabla WishList
"""

from rest_framework.parsers import JSONParser
from applications.ecommerce.models import WishList
from applications.ecommerce.comics.serializers import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

wish_responses = {
    "200": openapi.Response(
        description='Operación exitosa',
        examples = {
            "id": 1,
            "user": 1,
            "comic": 1,
            "favorite": "true",
            "cart": "true",
            "on_cart_qty": 10
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

def validate_user(request, user_id):
    """
    Función que se utiliza para validar que el token recibido pertenece al usuario al que se está queriendo acceder
    """
    try:
        user = User.objects.get(id=user_id)
    except:
        return None

    return Token.objects.get(key = request.headers.get("Authorization").split(" ")[1]).user == user


class GetWishListAPIView(ListAPIView):
    __doc__ = """
    GetWishListAPIView \n

    **Vista de API para administradores** \n

    Vista de API genérica que recibe peticiones de tipo GET para obtener una lista de todas las wishlists presentes en la base de datos. \n

    **Importante: el método post sólo puede ser utilizado por administradores de la aplicación.** \n
    """
    queryset = WishList.objects.all()
    serializer_class = GetWishListSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(auto_schema = None,tags = ["Administrador"], responses = wish_responses)

    def get(self, requests, *args, **kwargs):
        return super().get(requests, *args, **kwargs)


class GetWishListByUserIDAPIView(ListAPIView):
    __doc__ = """
    GetWishListByUserIDAPIView \n

    Vista de API genérica que devuelve una lista de todas las wishlists de un usuario. \n

    Es posible solicitar wishlists que estén en carrito y/o favoritos, enviando los valores por url de la siguiente forma:
    **?cart=true&favorite=true** \n

    _Nota: los posibles valores son **true** y **false**, y son independientes entre ellos, cualquiera de los dos puede ser **true** o **false** según
    lo que se necesite_

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario
    a actualizar en el campo **Authorization**.\n

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario 
    en el campo **Authorization**.\n
    """
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        user = User.objects.get(id = uid)

        try:
            cart = True if self.request.GET.get("cart").lower() == "true" else False if self.request.GET.get("cart").lower() == "false" else None
        except:
            cart = None

        try:
            favorite = True if self.request.GET.get("favorite").lower() == "true" else False if self.request.GET.get("favorite").lower() == "false" else None
        except:
            favorite = None

        wish = WishList.objects.filter(user=user)
        if type(cart) == bool:
            wish = WishList.objects.filter(cart=cart)
        if type(favorite) == bool:
            wish = wish.filter(favorite=favorite)

        return wish

    cart = openapi.Parameter('cart', openapi.IN_QUERY,
                        description="Traer wishlist con la condición de que esté en carrito (true o false)",
                        type=openapi.TYPE_BOOLEAN)

    favorite = openapi.Parameter('favorite', openapi.IN_QUERY,
                description="Traer wishlist con la condición de que esté en favorito (true o false)",
                type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(tags = ["Comics y Wishlists"], responses = wish_responses, manual_parameters=[cart, favorite])

    def get(self, request, *args, **kwargs):
        uid = self.kwargs.get("uid")

        try:
            User.objects.get(id = uid)
        except Exception as e:
            print(e)
            return Response(status = 400, data = {"error":"Bad request", "detail": f"No existe el usuario {uid}"})

        # Validar que el user id coincide con el token enviado
        if not validate_user(self.request, self.kwargs.get("uid")):
            return Response(status=401, data = {"error": "Unauthorized", "detail": "Credenciales inválidas - Token inválido"})
        
        return super().get(request, *args, **kwargs)


class PostWishListAPIView(CreateAPIView):
    __doc__ = f'''
    PostWishListAPIView \n

    Esta vista de API nos permite hacer un insert de una wishlist en la base de datos. \n

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario
    a dueño de la wishlist en el campo **Authorization**.\n
    '''
    queryset = WishList.objects.all()
    parser_classes = [JSONParser]
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(tags = ["Comics y Wishlists"], responses = wish_responses)

    def post(self, request, *args, **kwargs):

        # Validar que el username coincide con el token enviado
        uid = self.request.data.get("user")

        if not validate_user(self.request, uid):
            return Response(status=401, data = {"error": "Unauthorized", "detail": "Credenciales inválidas - Token inválido"})

        return super().post(request, *args, **kwargs)


class UpdateWishListAPIView(UpdateAPIView):
    __doc__ = f"""
    UpdateWishListAPIView \n
    
    Vista de API genérica para actualizar una wishlist vía peticiones de tipo **PATCH**. \n
    
    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario
    a dueño e la wishlist a actualizar en el campo **Authorization**.\n
    """

    queryset = WishList.objects.all()
    parser_classes = [JSONParser]
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return WishList.objects.filter(id=self.kwargs.get("pk"))

    @swagger_auto_schema(tags = ["Comics y Wishlists"], responses = wish_responses)

    def patch(self, request, *args, **kwargs):
        try:
            JSONParser().parse(request)
        except:
            return Response(status = 400, data = {"error": "Bad Request", "detail": "El payload no es un JSON válido"})
        
        # Validar que el username coincide con el token enviado
        uid = self.request.data.get("user")
        print("Validando", uid)
        if not validate_user(self.request, uid):
            return Response(status=401, data = {"error": "Unauthorized", "detail": "Credenciales inválidas - Token inválido"})

        return super().patch(request, *args, **kwargs)

    # No admitir requests de tipo put
    @swagger_auto_schema(auto_schema = None)
    def put(self, request, *args, **kwargs):
        return Response(status=405, data = {"error": "Method not allowed", "detail": "No se permite el uso de este método"})


class DeleteWishListAPIView(DestroyAPIView):
    __doc__ = f"""
    DeleteWishListAPIView \n

    Vista de API genérica para eliminar una wishlist vía peticiones de tipo **DELETE**. \n

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario
    dueño de la wishlist a eliminar en el campo **Authorization**.\n
    """

    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(tags = ["Comics y Wishlists"], responses = wish_responses)

    def delete(self, request, *args, **kwargs):
        # Validar que el username coincide con el token enviado
        try:
            uid = WishList.objects.get(id=self.kwargs.get("pk")).user.id
            if not validate_user(self.request, uid):
                return Response(status=401, data = {"error": "Unauthorized", "detail": "Credenciales inválidas - Token inválido"})
        
        except Exception as e:
            print(e)
            return Response(status=400, data = {"error": "Bad request", "detail": "No existe la wishlist a eliminar"})

        if super().delete(request, *args, **kwargs).status_code == 204:
            return Response(status=204, data = {"detail": "Wishlist eliminada correctamente"})


class CheckoutAPIView(APIView):
    __doc__ = f"""
    CheckoutAPIView \n

    Vista de API personalizada eliminar el carrito de un usuario luego de que el mismo realice una compra \n

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario 
    en el campo **Authorization**.\n
    """

    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        user = User.objects.get(id = uid)

        return WishList.objects.filter(user=user).filter(cart=True)

    del_responses = {
        204: openapi.Response(description = "Wishlists eliminadas correctamente")
    }
    del_responses.update(wish_responses)

    @swagger_auto_schema(tags = ["Comics y Wishlists"], responses = del_responses)

    def delete(self, request, *args, **kwargs):
        uid = self.kwargs.get("uid")
        try:
            user = User.objects.get(id = uid)
        except Exception as e:
            print(e)
            return Response(status = 400, data = {"error":f"No se encontró el usuario {uid}"})

        # Validar que el user id coincide con el token enviado
        if not validate_user(request, self.kwargs.get("uid")):
            return Response(status=401, data = {"error": "Unauthorized", "detail": "Credenciales inválidas - Token inválido"})
        
        for wish in self.get_queryset():
            wish.delete()

        return Response(status = 200, data = {"detail": "Wishlist eliminadas"})
    