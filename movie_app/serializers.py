from rest_framework import serializers
from movie_app.models import Movie, Review, Director
from django.db.models import Avg
from rest_framework.exceptions import ValidationError

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title reviews rating'.split()

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(avg_stars=Avg('stars'))['avg_stars']
        return round(avg_rating, 1) if avg_rating else None

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

    def get_movies_count(self, obj):
        return obj.movies.count()
    
class DirectorsValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=100)
    
class MoviesValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=100)
    description = serializers.CharField()
    duration = serializers.IntegerField(min_value=1)
    director_id = serializers.IntegerField()
    
    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise ValidationError("Director doesn't exist")
        return director_id
    
class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=255)
    movie_id = serializers.IntegerField(min_value=1)
    stars = serializers.IntegerField()
    
    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except:
            raise ValidationError("Movie doesn't exist")
        return movie_id
    
    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise ValidationError("Stars must be between 1 and 5.")
        return value
        
    
    
