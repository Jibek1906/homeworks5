from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from rest_framework import status
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

@api_view(['GET'])
def movies_api_list_view(request):
    movies = Movie.objects.select_related('director').prefetch_related('reviews')
    data = MovieSerializer(instance=movies, many=True).data
    return Response(data=data)

@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = MovieSerializer(instance=movie, many=False).data
    return Response(data=data)

@api_view(['GET'])
def directors_api_list_view(request):
    directors = Director.objects.all()
    data = DirectorSerializer(instance=directors, many=True).data
    return Response(data=data)

@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = DirectorSerializer(instance=director, many=False).data
    return Response(data=data)

@api_view(['GET'])
def reviews_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(instance=reviews, many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review Not Exist'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(instance=review, many=False).data
    return Response(data=data)

@api_view(['GET'])
def movies_reviews_api_view(request):
    movies = Movie.objects.select_related('director').prefetch_related('reviews')
    data = MovieSerializer(instance=movies, many=True).data
    return Response(data=data)