from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from datetime import date
from django.views.generic import FormView, ListView
from .models import Room, Booking, UserProfile
from .forms import AvailabilityForm, NewUserForm, RoomSearchForm, RoomForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import razorpay

razorpay_client = razorpay.Client(auth=('rzp_test_nzs4ByTHntmX6Z', 'royYN10eUq420ptrsRtrqtpE'))
RAZORPAY_PAYMENT_METHODS = ['card', 'netbanking', 'upi']
RAZORPAY_API_KEY = "rzp_test_nzs4ByTHntmX6Z"



def check_availability(room, check_in, check_out):
    booking_list = Booking.objects.all()
    available_list = []

    for booking in booking_list :
        if booking.check_out < date.today():
            booking.delete()

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
        if form.is_valid():
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

def BookSelection(request, number, check_in, check_out) :
    check_in_date = check_in
    check_out_date = check_out
    roomDetail = Room.objects.get(number = number)
    booking = Booking.objects.create(user=request.user, room=roomDetail, check_in=check_in_date, check_out=check_out_date)
    booking.save()
    context = {'booking' : booking}
    return render(request, 'success_booking.html', context)

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST, request.FILES)
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
                messages.success(request, f"you are now logged in as {username}.")
                return redirect("home")
            else :
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("home")

def room_search_view(request):
    if request.method == 'POST':
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['room_category']
            check_in_date = form.cleaned_data['check_in']
            check_out_date = form.cleaned_data['check_out']

            # filter rooms based on user selections
            rooms = Room.objects.filter(category=category)
            available_rooms = []

            for room in rooms :
                if check_availability(room, check_in_date, check_out_date):
                    available_rooms.append(room)

            context = {'rooms' : available_rooms, 'category' : category, 'check_in' : check_in_date, 'check_out' : check_out_date}
            return render(request, 'room_search_results.html', context)
    else:
        form = RoomSearchForm()
    return render(request, 'room_search.html', {'form': form})

def manage_room(request):
    return render(request, 'managerooms.html')

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save()
            return redirect('room_detail', number=room.number)
    else:
        form = RoomForm()
    return render(request, 'room_form.html', {'form': form})

def delete_room(request):
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request, "deletion_list_view.html", context)

def room_detail(request, number):
    room = Room.objects.get(number=number)
    context = {'room': room}
    return render(request, 'room_detail.html', context)

def deleteRoom(request, number):
    room = Room.objects.get(number=number)
    room.delete()
    return HttpResponse("Room deleted successfully")

def profile_page(request):
    user = UserProfile.objects.get(username=request.user.username)

    context = {'user' : user}
    return render(request, "profile_page_view.html", context)

def about(request):
    return render(request, "about.html")
def contact_us(request):
    return render(request, "contact_us.html")



def book_now(request, number, check_in, check_out):
    # Retrieve the room and booking details from the request
    # room_number = request.GET.get('room_number')
    # check_in_date = request.GET.get('check_in')
    # check_out_date = request.GET.get('check_out')

    # Create a Razorpay order with the amount and other details
    room = Room.objects.get(number=number)
    order_amount = room.room_price # Replace with the actual amount
    print(order_amount)
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'

    razorpay_order = razorpay_client.order.create(dict(amount=(order_amount * 100), currency=order_currency, receipt=order_receipt, payment_capture=1))

    # Render the payment form with the order details
    return render(request, 'payment_form.html', {'order_id': razorpay_order['id'], 'amount': order_amount, 'currency': order_currency})

def success_payment_page(request):
    booking = Booking.objects.create()
    messages.success(request, "Payment Was Successfull")
    return 
