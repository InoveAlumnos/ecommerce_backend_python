#!/usr/bin/env python

'''
Permisos y formas de autenticación custom!
'''

from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _

class IsClient(BasePermission):
    """
    Permitir acceso solo a usuarios del grupo `client`
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name = "client").exists())
