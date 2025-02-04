from rest_framework import serializers
from .models import Listing, Booking, Review


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'start_date', 'end_date', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'listing', 'user', 'rating', 'comment', 'created_at']

class ListingSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price', 'location', 'host', 'created_at', 'updated_at', 'reviews']
