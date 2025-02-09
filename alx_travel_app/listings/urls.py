from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, ReviewViewSet, PaymentVerificationViewSet



# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('payment/verify/<str:transaction_id>/', PaymentVerificationViewSet.as_view({'get': 'verify_payment'}), name='verify_payment'),
    path('', include(router.urls)),  # Include the router's URLs
]