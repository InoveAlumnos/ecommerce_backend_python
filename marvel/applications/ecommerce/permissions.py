#!/usr/bin/env python

'''
Permisos y formas de autenticación custom!
'''

from unidecode import unidecode
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.utils.translation import gettext_lazy as _

class IsClient(BasePermission):
    """
    Allows access only to Client Group users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name = "client").exists())
