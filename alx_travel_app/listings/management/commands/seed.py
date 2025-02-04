from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from alx_travel_app.listings.models import Listing, Booking, Review
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        # Create a sample user
        user = User.objects.create_user(username='testuser', password='testpass123')
        host = User.objects.create_user(username='hostuser', password='hostpass123')

        # Create sample listings
        listings = []
        for i in range(5):
            listing = Listing.objects.create(
                title=f'Beautiful Apartment {i+1}',
                description=f'A cozy apartment in the heart of the city {i+1}',
                price=random.randint(50, 200),
                location=f'City {i+1}',
                host=host
            )
            listings.append(listing)

        # Create sample bookings
        for listing in listings:
            Booking.objects.create(
                listing=listing,
                user=user,
                start_date=datetime.now().date(),
                end_date=(datetime.now() + timedelta(days=random.randint(1, 7))).date()
            )

        # Create sample reviews
        for listing in listings:
            Review.objects.create(
                listing=listing,
                user=user,
                rating=random.randint(1, 5),
                comment=f'Great experience at {listing.title}!'
            )


        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))