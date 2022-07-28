#!/usr/bin/env python

from django.urls import path
from e_commerce.api.marvel_api_views import *
from e_commerce.auth.login import LoginUserAPIView
from e_commerce.auth.signup import SignUpUserAPIView

urlpatterns = [
    path('user/login/', LoginUserAPIView.as_view()),
    path("user/signup/", SignUpUserAPIView.as_view()),
]