from django.urls import path
from movie_app.views import (
    DirectorListCreateAPIView, DirectorDetailAPIView,
    MovieViewSet, ReviewListCreateAPIView, ReviewDetailAPIView
)

urlpatterns = [
    path('directors/', DirectorListCreateAPIView.as_view(), name='directors-list'),
    path('directors/<int:id>/', DirectorDetailAPIView.as_view(), name='director-detail'),
    path('movies/', MovieViewSet.as_view(
        {'get': 'list', 'post': 'create'}), 
         name='movies-list'),
    path('movies/<int:id>/', MovieViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), 
         name='movie-detail'),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='reviews-detail'),
]
