from rest_framework import serializers
from movie_app.models import Movie, Review, Director
from django.db.models import Avg

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
