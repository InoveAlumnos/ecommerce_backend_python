#!/usr/bin/env python


'''
Hacer un fetch de los comics de la API de marvel en nuestra database
'''


from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from e_commerce.api.marvel_api_views import *
from e_commerce.models import Comic
import requests


@permission_classes((IsAuthenticated, IsAdminUser))
@api_view(["PATCH"])
def fetch_db(request):
    
    # Limpiar tabla actual de comics
    Comic.objects.all().delete()

    # Obtener comics usando la API de marvel
    params = PARAMS  # Realizo esta asignación para luego actualizar el valor de params con offset 
    params.update({'limit': 20, 'offset': 0})
    comics = requests.get(URL_BASE + ENDPOINT, params = params)
    
    if comics.status_code > 300 or not comics.json().get('data').get('results'):
        # Devolver internal server error - status code 500
        print("Error al obtener los comics: " + str(comics.status_code))
        return Response({"error": "Error al obtener los comics"}, status=500)

    # Guardar comics en la base de datos - Se usa el offset como parámetro para saber cuando dejar de cargar comics
    comics_cargados = 0

    while True:
        for comic in comics.json().get('data').get('results'):

            # Obtener valores del comic
            comic_id = comic.get('id')
            comic_title = comic.get('title') if comic.get('title') else "Not available"
            comic_description = comic.get('description') if comic.get('description') else "Not available"
            comic_price = comic.get('prices')[0].get('price') if comic.get('prices')[0].get('price') else 0

            # Proteger esta sección para evitar errores en caso de no encontrar la imagen
            try:
                comic_thumbnail = comic.get('thumbnail').get('path') + "/standard_xlarge.jpg" if comic.get('thumbnail') else 'Not Available'
            except:
                comic_thumbnail = None

            # try-catch para marvel_ids repetidos
            try:
                Comic.objects.create(marvel_id = comic_id, title = comic_title, description = comic_description, price = comic_price, stock_qty = 100, picture = comic_thumbnail)

            except Exception as e:
                print(f"Se omitió comic duplicado: {comic_title} - {comic_id}")
                continue
                
            comics_cargados += 1

            if comics_cargados >= 300:
                return Response({"success": "Se guardaron los comics en la base de datos"}, status=200)
                
        
        # Actualizar offset
        params.update({'offset': params.get('offset') + 20})
        
        # Obtener más comics desde API
        comics = requests.get(URL_BASE + ENDPOINT, params = PARAMS)

        # Si recibimos una lista vacía, terminamos - no hay más comics que obtener
        if not comics.json().get('data').get('results'):
            return Response({"success": "Se guardaron los comics en la base de datos"}, status=200)
    