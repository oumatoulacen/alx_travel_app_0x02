from django.contrib import admin
from .models import Booking, Listing, Payment, Review

admin.site.register(Listing)
admin.site.register(Review)
admin.site.register(Booking)
admin.site.register(Payment)
