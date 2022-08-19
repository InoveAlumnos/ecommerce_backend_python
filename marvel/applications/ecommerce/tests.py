#!/usr/bin/env python

from django.test import TestCase

class AuthTest(TestCase):
    """
    Clase de prueba para la autenticación de usuarios
    """

    def login_client_test(self):
        """
        Test endpoint: [POST] /client/login
        """
        endpoint = "/client/login"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "username": "testclient",
            "password": "testclient"
        }

        # Caso de éxito
        response = self.client.post(endpoint, headers = headers, data = data)
        self.assertEqual(response.status_code, 200)

        # Caso de error: no se envia header con Content-Type
        response = self.client.post(endpoint, data = data)
        self.assertEqual(response.status_code, 500)

        # Caso de error: contraseña incorrecta
        data.update({"password": "wrongpassword"})
        response = self.client.post(endpoint, headers = headers, data = data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get("detail"), "Credenciales inválidas")
