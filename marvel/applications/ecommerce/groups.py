#!/usr/bin/env python

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from psycopg2 import IntegrityError

class ClientGroupMeta(type):
    _instancias = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            instancia = super().__call__(*args, **kwargs)
            cls._instancias[cls] = instancia
        
        return cls._instancias[cls]


class GenericGroup:
    def agregar_usuario(self, usuario):
        self.group.user_set.add(usuario)

    def eliminar_usuario(self, usuario):
        self.group.user_set.remove(usuario)

    def agregar_usuario_username(self, username: str):
        try:
            self.group.user_set.add(User.objects.get(username=username))
        except User.DoesNotExist:
            print(f"No se pudo agregar al usuario {username} porque no existe")


class ClientGroup(GenericGroup, metaclass = ClientGroupMeta):
    """
    Clase Singleton - De única instancia
    """
    try:
        group, _ = Group.objects.get_or_create(name = "client") 
    except:
        print("Es necesario realizar migraciones")
        pass        


class ConsumerGroup(GenericGroup, metaclass = ClientGroupMeta):
    """
    Clase Singleton - De única instancia
    """
    try:
        group, _ = Group.objects.get_or_create(name = "consumer") 
    except:
        print("Es necesario realizar migraciones")
        pass
    

class ConsumerGroup(GenericGroup, metaclass = ClientGroupMeta):
    """
    Clase Singleton - De única instancia
    """
    try:
        group, _ = Group.objects.get_or_create(name = "test") 
    except:
        print("Es necesario realizar migraciones")
        pass
