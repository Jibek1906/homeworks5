from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from rest_framework import status
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, DirectorsValidateSerializer, MoviesValidateSerializer, ReviewValidateSerializer
from django.db import transaction

@api_view(['GET', 'POST'])
def movies_list_create_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.select_related('director').prefetch_related('reviews')
        data = MovieSerializer(instance=movies, many=True).data
        return Response(data={'list': data})
    elif request.method == 'POST':
        serializer = MoviesValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
            
        title = serializer.validated_data.get('title', None)
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
        
        with transaction.atomic():
            director = Director.objects.get(id=director_id)
            movie = Movie.objects.create(
                title=title,
                description=description,
                duration=duration,
                director=director,
            )

        return Response(data={'movie_id': movie.id},status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(instance=movie, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MoviesValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        movie.title = serializer.validated_data.get('title', None)
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director = Director.objects.get(id=serializer.validated_data.get('director_id'))
        movie.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def directors_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(instance=directors, many=True).data
        return Response(data={"list": data})
    elif request.method == 'POST':
        serializer = DirectorsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        print(request.data)
        name = serializer.validated_data.get('name')
        director = Director.objects.create(
            name=name,
        )
        return Response(data={'director_id': director.id},status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(instance=director, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def reviews_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(instance=reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
            
        text = serializer.validated_data.get('text')
        movie_id = serializer.validated_data.get('movie_id', None)
        stars = serializer.validated_data.get('stars')
        
        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                movie_id=movie_id,
                stars=stars,
            )
        return Response(data={'review_id': review.id}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review Not Exist'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(instance=review, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
            
        review.text = serializer.validated_data.get('text')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.stars = serializer.validated_data.get('stars')
        review.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def movies_reviews_api_view(request):
    movies = Movie.objects.select_related('director').prefetch_related('reviews')
    data = MovieSerializer(instance=movies, many=True).data
    return Response(data=data)