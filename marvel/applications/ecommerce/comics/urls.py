#!/usr/bin/env python

"""applications.ecommerce.comics URL Configuration

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

from django.urls import path
from applications.ecommerce.comics.comics import *
from applications.ecommerce.comics.wish import *
from applications.ecommerce.comics.fetch import FetchDatabaseAPIView

urlpatterns = [
    # APIs de Marvel
    path('comics/fetch-database', FetchDatabaseAPIView.as_view(), name='fetch-database'),
    
    # Comic API View:
    path('comics/get', GetComicAPIView.as_view(),),
    path('comics/post', PostComicAPIView.as_view()),
    path('comics/get-post', ListCreateComicAPIView.as_view()),
    path('comics/<pk>/update', RetrieveUpdateComicAPIView.as_view()),
    path('comics/<pk>/delete', DestroyComicAPIView.as_view()),

    # WishList API View
    path('wish/get', GetWishListAPIView.as_view()),
    path('wish/post', PostWishListAPIView.as_view()),
    path("wish/get/<uid>", GetWishListByUserIDAPIView.as_view()),
    path('wish/purchase/<uid>', PurchaseAPIView.as_view()),
    path('wish/<pk>/update', UpdateWishListAPIView.as_view()),
    path('wish/<pk>/delete', DeleteWishListAPIView.as_view()),
]
