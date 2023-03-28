from django.contrib import admin
from .models import Room, Booking, UserProfile, BookingHistory

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(BookingHistory)


