#!/usr/bin/env python

"""applications.ecommerce URL Configuration

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
from django.urls import path
from applications.ecommerce.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(
                    template_name='ecommerce/login.html', 
                    redirect_authenticated_user=True, 
                    redirect_field_name='index'
                    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
                    next_page='/ecommerce/',  
                    redirect_field_name='index'), name='logout'),
         
    path('signup/', register, name = 'register'),

    # NOTE: Site pages
    path('', IndexView.as_view(), name='index'),  # Index view
    
    path('tutorial/', TutorialView.as_view(), name='tutorial'),  # Index view
    
]