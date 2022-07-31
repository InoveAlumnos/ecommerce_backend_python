#!/usr/bin/env python

"""applications.ecommerce.auth URL Configuration

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

from django.urls import path, include
from applications.ecommerce.auth.login import LoginClientAPIView, LoginUserAPIView
from applications.ecommerce.auth.signup import SignUpClientAPIView, SignUpUserAPIView
from applications.ecommerce.auth.reset import ResetPasswordView
from applications.ecommerce.auth.profile import UpdateProfileAPIView

urlpatterns = [
    path('user/login/', LoginUserAPIView.as_view()),
    path("user/signup/", SignUpUserAPIView.as_view()),
    path("user/reset-password/", ResetPasswordView.as_view()),
    path("user/profile/update/", UpdateProfileAPIView.as_view()),
    path("client/login/", LoginClientAPIView.as_view()), 
    path("client/signup/", SignUpClientAPIView.as_view()),
    # path('client/forgot-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
