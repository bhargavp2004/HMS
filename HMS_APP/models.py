from django.db import models
from django.conf import settings

class Room(models.Model) :
    ROOM_CATEGORIES = (
        ('WithAc', 'AC'),
        ('WithoutAc', 'NON-AC'),
        ('Deluxe', 'DELUXE'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length = 10, choices=ROOM_CATEGORIES)
    capacity = models.IntegerField()

    def __str__(self) :
        return f'Room number {self.number} is having capacity of {self.capacity} people and category is {self.category}'
    
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self) :
        return f'{self.user} has booked room with {self.room} from {self.check_in} to {self.check_out}'