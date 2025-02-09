from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth.models import User
from django.urls import path
from .models import Listing, Booking, Review, Payment
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer, PaymentSerializer, UserSerializer
import requests
import uuid
from django.conf import settings


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        self.process_payment(booking)

    def process_payment(self, booking):
        transaction_id = str(uuid.uuid4())  # Generate unique transaction ID
        payment_data = {
            "amount": str(booking.listing.price),
            "currency": "ETB",
            "email": booking.user.email,
            "tx_ref": transaction_id,
            "return_url": f"http://127.0.0.1:8000/api/payment/verify/{transaction_id}/",
        }

        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        response = requests.post(chapa_url, json=payment_data, headers=headers)
        print("verify_payment", f"http://127.0.0.1:8000/api/payment/verify/{transaction_id}/")
        if response.status_code == 200:
            Payment.objects.create(
                booking=booking,
                transaction_id=transaction_id,
                amount=booking.listing.price,
                status='pending'
            )
        else:
            booking.delete()
            raise Exception("Payment initialization failed")


class PaymentVerificationViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def verify_payment(self, request, transaction_id):
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        chapa_url = f"https://api.chapa.co/v1/transaction/verify/{transaction_id}"
        response = requests.get(chapa_url, headers=headers)

        if response.status_code == 200:
            payment_status = response.json().get("status")
            try:
                payment = Payment.objects.get(transaction_id=transaction_id)
                if payment_status == "success":
                    payment.status = "completed"
                else:
                    payment.status = "failed"
                payment.save()
                return Response({"message": "Payment status updated", "status": payment.status}, status=status.HTTP_200_OK)
            except Payment.DoesNotExist:
                return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Failed to verify payment"}, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
