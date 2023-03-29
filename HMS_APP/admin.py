from django.contrib import admin
from .models import Payment, Room, Booking, UserProfile, BookingHistory

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(BookingHistory)
admin.site.register(Payment)

