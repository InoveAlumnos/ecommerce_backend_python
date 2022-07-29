#!/usr/bin/env python

from django.contrib.auth.models import Group


class ClientGroupMeta(type):
    _instancias = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            instania = super().__call__(*args, **kwargs)
            cls._instancias[cls] = instania
        
        return cls._instancias[cls]


class ClientGroup(metaclass = ClientGroupMeta):
    """
    Clase Singleton - De única instancia
    """
    group, _ = Group.objects.get_or_create(name = "Client") 

    def agregar_usuario(self, usuario):
        self.group.user_set.add(usuario)
