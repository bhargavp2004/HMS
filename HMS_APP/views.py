from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
import datetime
from django.views.generic import FormView, ListView
from .models import Room, Booking
from .forms import AvailabilityForm, NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

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

def showDetails(request):
    RoomDetails = Room.objects.all()
    context = {'roomDetails' : RoomDetails}
    return render(request, 'details.html', context)        

def BookSelection(request, number) :
    roomDetail = Room.objects.filter(id = number)
    context = {'SpecificDetail' : roomDetail}
    return render(request, 'SpecificBooking.html', context)

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request) :
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"you are now logged in as {username}.")
                return redirect("home")
            else :
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")