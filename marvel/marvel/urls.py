"""marvel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


# Docs description - Swagger - OpenAPI
description = '''
<img src="https://lh3.googleusercontent.com/pw/AM-JKLWLct73ne_PgqQ146YMYjUgbswqg703xPZPnVImkFYwGbao5YksFGJFOlcoCJLfqIJ9_LRwFAwP9qinoEvsLx92NTOfAn54SgMLTgMvtii0r_rjneGjR53bx08OCncv4mRH4gNnpmEUuKofj59L9dAv=w1257-h103-no?authuser=0">
<h2>Documentación general de APIs de la aplicación ecommerce</h2>
'''

schema_view = get_schema_view(
    openapi.Info(
        title="Inove Marvel e-commerce",
        default_version='1.0.0',
        description=description,
        contact=openapi.Contact(email="info@inove.com.ar"),
        license=openapi.License(name="Inove Coding School."),
    ),
    public=True,
    permission_classes= [],
    authentication_classes= []
)

urlpatterns = [
    # Redirecciones
    path('', lambda request: redirect('/ecommerce/', permanent=True)),
    path('/', lambda request: redirect('/ecommerce/', permanent=True)),
    path('api-docs/', lambda request: redirect("/api-docs/swagger", permanent=True)),
    
    # Administrador de db
    path('admin/', admin.site.urls),

    # ecommerce
    path('ecommerce/', include('applications.ecommerce.urls')),
    path('ecommerce/', include('applications.ecommerce.auth.urls')),
    path('ecommerce/', include('applications.ecommerce.comics.urls')),

    # api-docs
    path('api-docs/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-docs/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
