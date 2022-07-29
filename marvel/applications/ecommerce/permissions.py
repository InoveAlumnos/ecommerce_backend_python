#!/usr/bin/env python

'''
Permisos custom!
'''

from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    """
    Allows access only to Client Group users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name = "Client").exists())
