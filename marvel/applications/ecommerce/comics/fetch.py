#!/usr/bin/env python

'''
Hacer un fetch de los comics de la API de marvel en nuestra database - Endpoint sólo para superusuarios
'''

import requests
import hashlib
from typing import List
from applications.ecommerce.models import Comic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

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
    __doc__ = f'''
    Esta vista de API nos permite hacer un fetch de los comics de la API de marvel en nuestra database.\n

    `[METODO PATCH]`
    Actualizar comics existentes \n
    
    `[METODO POST]`
    Eliminar todos los comics y agregar otros 300 comics \n
    '''

    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]


    def post(self, request, *args, **kwargs):
        '''
        Al usar el método POST, se sobrescribe la DB, se eliminan todos los comics anteriores
        '''
        # Eliminar todos los comics anteriores
        Comic.objects.all().delete()

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


    def patch(self, request, *args, **kwargs):
        '''
        Al usar el método PATCH, se agrega a la DB los comics que no están en la DB
        '''
        # Obtener comics
        offset = 0
        comics_guardados = 0

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

        except Exception as e:
            print(e)
            return Response(status = 500, data = {"error": "Internal server error"})


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
            picture = comic_thumbnail
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
