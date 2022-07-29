#!/usr/bin/env python

from django.contrib.auth.models import Group
from django.core.management import execute_from_command_line


class ClientGroupMeta(type):
    _instancias = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            instancia = super().__call__(*args, **kwargs)
            cls._instancias[cls] = instancia
        
        return cls._instancias[cls]


class ClientGroup(metaclass = ClientGroupMeta):
    """
    Clase Singleton - De única instancia
    """
    try:
        group, _ = Group.objects.get_or_create(name = "Client") 
    except:
        execute_from_command_line("python marvel/manage.py makemigrations ecommerce")
        execute_from_command_line("python marvel/manage.py migrate ecommerce")
        
    def agregar_usuario(self, usuario):
        self.group.user_set.add(usuario)
