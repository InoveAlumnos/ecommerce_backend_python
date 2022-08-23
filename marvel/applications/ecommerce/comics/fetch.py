#!/usr/bin/env python

'''
Hacer un fetch de los comics de la API de marvel en nuestra database - Endpoint sólo para superusuarios
'''

import requests
import hashlib
import random
from typing import List
from applications.ecommerce.models import Comic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# TODO: Mover estas keys a variables de entorno
PUBLIC_KEY = '58ee40376f7c10e99f440f5e3abd2caa'
PRIVATE_KEY = '2c0373e00d85edb4560f68ddc2094014e8694f90'
TS = 1
TO_HASH = str(TS)+PRIVATE_KEY+PUBLIC_KEY
HASHED = hashlib.md5(TO_HASH.encode())
URL_BASE = 'http://gateway.marvel.com/v1/public/'
ENDPOINT = 'comics'
PARAMS = dict(ts=TS, apikey=PUBLIC_KEY, hash=HASHED.hexdigest())


class Fin(Exception): 
    '''
    Clase auxiliar para cortar abruptamente ciclo de búsqueda con bucles anidados
    '''
    pass


class FetchDatabaseAPIView(APIView):
    __doc__ = f"""
    FetchDatabaseAPIView \n

    **Vista de API para administradores** \n

    Esta vista de API nos permite hacer un fetch de los comics de la API de marvel en nuestra database.\n
    """

    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(tags = ["Administrador"])

    def post(self, request, *args, **kwargs):
        # Eliminar todos los comics anteriores
        Comic.objects.all().delete()

        # precio 0 - stock 0

        # Obtener comics
        comics_guardados = 0
        offset = 0
        try: 
            while True:
                comics = self.get_comics(offset = offset)

                # Guardar comics en la DB
                for comic in comics:
                    try:
                        comic.save()
                        comics_guardados += 1
                    
                    except Exception as e:
                        print(e)
                        continue

                    if comics_guardados >= 300:
                        # Lanzo una excepción para cortar abruptamente ambos bucles (while y for)
                        raise Fin("Se guardaron 300 comics")

                offset += 20

        except Fin:
            return Response({"response": "Comics actualizados"}, status=200)


    def dict_to_comic(self, comic: dict = {}) -> Comic:
        # Obtener valores del comic
        comic_id = comic.get('id')
        comic_title = comic.get('title') if comic.get('title') else "Not available"
        comic_description = comic.get('description') if comic.get('description') else "Not available"
        comic_price = comic.get('prices')[0].get('price') if comic.get('prices')[0].get('price') else 0

        # Proteger esta sección para evitar errores en caso de no encontrar la imagen
        try:
            comic_thumbnail = comic.get('thumbnail').get('path') + "/standard_xlarge.jpg" if comic.get('thumbnail') else 'Not Available'
        except:
            # Omitir comics que no tienen foto
            return None
        
        return Comic(
            marvel_id = comic_id,
            title = comic_title,
            description = comic_description,
            price = comic_price,
            stock_qty = 100,
            picture = comic_thumbnail,
            stars = random.randint(1, 5)
        )


    def get_comics(self, limit: int = 20, offset: int = 0) -> List[Comic]:
        # Obtener comics usando la API de marvel
        params = PARAMS  # Realizo esta asignación para luego actualizar el valor de params con offset 
        params.update({'limit': limit, 'offset': offset})
        comics = requests.get(URL_BASE + ENDPOINT, params = params)
    
        if comics.status_code > 300 or not comics.json().get('data').get('results'):
            # Devolver internal server error - status code 500
            print(f"Error al obtener los comics: {str(comics.status_code)} - {str(comics.content)}")
            return Response({"error": "Error al obtener los comics"}, status=500)
        
        return [self.dict_to_comic(comic) for comic in comics.json().get('data').get('results') if self.dict_to_comic(comic)]
