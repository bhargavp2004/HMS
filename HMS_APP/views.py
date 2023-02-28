from urllib import request
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import datetime
from django.views.generic import FormView, ListView
from .models import Room, Booking
from .forms import AvailabilityForm

def check_availability(room, check_in, check_out):
    available_list = []
    booking_list = Booking.objects.filter(room=room)

    for booking in booking_list :
        if booking.check_in > check_out or booking.check_out < check_in :
            available_list.append(True)
        else:
            available_list.append(False)

    return all(available_list)

class RoomList(ListView):
    model = Room


class BookingList(ListView):
    model = Booking

def home(request):
    return render(request, 'index.html')

class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(category = data['room_category'])
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )        
            booking.save()
            return HttpResponse(booking)
        else :
            return HttpResponse("Rooms are not available")            

        

