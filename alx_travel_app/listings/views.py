from rest_framework import viewsets
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.prefetch_related('reviews')
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can create/update listings

    def perform_create(self, serializer):
        # Automatically set the host to the current user
        serializer.save(host=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can create/update bookings

    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can create/update reviews

    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)
