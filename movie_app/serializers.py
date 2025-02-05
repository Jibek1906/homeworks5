from rest_framework import serializers
from movie_app.models import Director, Movie, Review

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'name'.split()

class MovieSerializer(serializers.ModelSerializer):
    director = serializers.CharField(source='director.name')
    
    class Meta:
        model = Movie
        fields = 'title description duration director'.split()

class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source='movie.title')
    
    class Meta:
        model = Review
        fields = 'text movie'.split()