from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from rest_framework import status
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, DirectorsValidateSerializer, MoviesValidateSerializer, ReviewValidateSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView 
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.db import transaction

class DirectorListCreateAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    
class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.select_related('director').prefetch_related('reviews')
    serializer_class = MovieSerializer
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        serializer = MoviesValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            director = Director.objects.get(id=serializer.validated_data['director_id'])
            movie = Movie.objects.create(
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description'],
                duration=serializer.validated_data['duration'],
                director=director,
            )
        return Response({'movie_id': movie.id}, status=status.HTTP_201_CREATED)
    
class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            review = Review.objects.create(**serializer.validated_data)
        return Response({'review_id': review.id}, status=status.HTTP_201_CREATED)

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer