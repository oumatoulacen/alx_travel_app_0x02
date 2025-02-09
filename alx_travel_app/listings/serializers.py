from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price', 'location', 'created_at', 'updated_at', 'host']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())  # Make listing selectable

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'start_date', 'end_date', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'listing', 'user', 'rating', 'comment', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'booking', 'transaction_id', 'amount', 'status', 'created_at']
