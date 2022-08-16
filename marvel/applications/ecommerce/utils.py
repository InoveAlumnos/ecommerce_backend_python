#!/usr/bin/env python

def dict_create_from_keys(dictionary, *keys):
    '''
    @NAME: dict_get_keys
    
    @DESC: Función para obtener las claves de un diccionario.
    
    @PARAMS:
        - dictionary: dict
        - keys: list
    
    @RETURN: dict
    '''
    return {key: dictionary.get(key, "None") for key in keys}
