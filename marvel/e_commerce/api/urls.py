from django.urls import path
from e_commerce.api.marvel_api_views import *

# Importamos las API_VIEWS:
from e_commerce.api.api_views import *
from e_commerce.api.fetch import FetchDatabaseAPIView

urlpatterns = [
    # APIs de Marvel
    path('get-comics/', get_comics, name='get-comics'),
    path('fetch-database/', FetchDatabaseAPIView.as_view(), name='fetch-database'),
    path('purchased-item/', purchased_item, name='purchased-item'),
    
    # CRUD Comic API View:
    path('comics/get', GetComicAPIView.as_view(),),
    path('comics/post', PostComicAPIView.as_view()),
    path('comics/get-post', ListCreateComicAPIView.as_view()),
    path('comics/<pk>/update', RetrieveUpdateComicAPIView.as_view()),
    path('comics/<pk>/delete', DestroyComicAPIView.as_view()),

    # TODO: Wish-list API View
    path('wish/get', GetWishListAPIView.as_view()),
    path('wish/post', PostWishListAPIView.as_view()),
    
    # TODO: Test API Logging:
    path('test-logging', TestLogAPIView.as_view()),

]