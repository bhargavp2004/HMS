from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(User):
    mobile_number = models.CharField(max_length=10)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'User registration done by {self.first_name} {self.last_name}'

class Room(models.Model) :
    ROOM_CATEGORIES = (
        ('WithAc', 'AC'),
        ('WithoutAc', 'NON-AC'),
        ('Deluxe', 'DELUXE'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length = 10, choices=ROOM_CATEGORIES)
    capacity = models.IntegerField()
    room_description = models.TextField()

    def __str__(self) :
        return f'Room number {self.number} is having capacity of {self.capacity} people and category is {self.category}'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self) :
        return f'{self.user} has booked room with {self.room} from {self.check_in} to {self.check_out}'

        #changed through vs code
