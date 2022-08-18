#!/usr/bin/env python

"""
APIs genéricas para realizar un CRUD a la base de datos - Tabla WishList
"""

from applications.ecommerce.models import WishList
from applications.ecommerce.comics.serializers import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView

def validate_user(request, user_id):
    """
    Función que se utiliza para validar que el token recibido pertenece al usuario al que se está queriendo acceder
    """
    user = User.objects.get(id=user_id)
    return Token.objects.get(key = request.headers.get("Authorization").split(" ")[1]).user == user


class GetWishListAPIView(ListAPIView):
    __doc__ = """
    GetWishListAPIView \n

    Vista de API genérica que recibe peticiones de tipo GET para obtener una lista de todas las wishlists presentes en la base de datos. \n

    **Importante: el método post sólo puede ser utilizado por administradores de la aplicación.** \n
    """
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class GetWishListByUserIDAPIView(ListAPIView):
    __doc__ = """
    Vista de API genérica que devuelve una lista de todas las wishlists de un usuario.

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

    def get(self, request, *args, **kwargs):
        uid = self.kwargs.get("uid")
        try:
            user = User.objects.get(id = uid)
        except Exception as e:
            print(e)
            return Response(status = 400, data = {"error":f"No se encontró el usuario {uid}"})

        # Validar que el user id coincide con el token enviado
        if not validate_user(self.request, self.kwargs.get("uid")):
            return Response(status=401, data = {"error": "Unauthorized", "message": "Credenciales inválidas - Token inválido"})
        
        return super().get(request, *args, **kwargs)


class PostWishListAPIView(CreateAPIView):
    __doc__ = f'''
    PostWishListAPIView \n

    Esta vista de API nos permite hacer un insert de una wishlist en la base de datos. \n
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # Validar que el username coincide con el token enviado
        if not validate_user(self.request, request.user):
            return Response(status=401, data = {"error": "Unauthorized", "message": "Credenciales inválidas - Token inválido"})

        return super().post(request, *args, **kwargs)


class PostWishListAPIView(ListCreateAPIView):
    __doc__ = f'''
    PostWishListAPIView \n

    Esta vista de API nos permite hacer un insert de una wishlist en la base de datos. \n
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # Validar que el username coincide con el token enviado
        if not validate_user(request, request.user):
            return Response(status=401, data = {"error": "Unauthorized", "message": "Credenciales inválidas - Token inválido"})

        return super().post(request, *args, **kwargs)


class PurchaseAPIView(APIView):
    __doc__ = f"""
    PurchaseAPIView \n

    Vista de API para personalizada eliminar las wishlists de un usuario luego de que el mismo realice una compra \n

    Para usar este endpoint, es necesario enviar la api-key en el header en el campo **X-Api-Key** y el token del usuario 
    en el campo **Authorization**.\n
    """

    permission_classes = [HasAPIKey and IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        user = User.objects.get(id = uid)

        return WishList.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        uid = self.kwargs.get("uid")
        try:
            user = User.objects.get(id = uid)
        except Exception as e:
            print(e)
            return Response(status = 400, data = {"error":f"No se encontró el usuario {uid}"})

        # Validar que el user id coincide con el token enviado
        if not validate_user(request, self.kwargs.get("uid")):
            return Response(status=401, data = {"error": "Unauthorized", "message": "Credenciales inválidas - Token inválido"})
        
        for wish in self.get_queryset():
            wish.delete()

        return Response(status = 200, data = {"message": "Wishlist eliminadas"})
