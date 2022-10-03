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
from applications.ecommerce.auth.profile import UpdateProfileAPIView, GetProfileDataByUserId

urlpatterns = [
    path('users/login', LoginUserAPIView.as_view()),
    path("users/signup", SignUpUserAPIView.as_view()),
    path("users/reset-password", ResetPasswordView.as_view()),
    path("users/profile/update/<uid>", UpdateProfileAPIView.as_view()),
    path("users/profile/get/<uid>", GetProfileDataByUserId.as_view()),
    path("clients/login", LoginClientAPIView.as_view()), 
    path("clients/signup", SignUpClientAPIView.as_view()),
    # path('client/forgot-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
