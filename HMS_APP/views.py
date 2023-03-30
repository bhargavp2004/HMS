from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import FormView, ListView
from .models import ImageGallery, Payment, Room, Booking, UserProfile, BookingHistory
from .forms import AvailabilityForm, ImageForm, NewUserForm, RoomSearchForm, RoomForm, UpdateInformationForm, UserUpdateInformationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import razorpay
import datetime
from datetime import date, datetime

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
            messages.success(request, "The room was added successfully!")
            return redirect("home")
    else:
        form = RoomForm()
    return render(request, 'room_form.html', {'form': form})

def delete_room(request):
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request, "deletion_list_view.html", context)

def update_room(request):
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request, "roomList.html", context)

def update_request(request,number):
    room = Room.objects.get(number=number)
    if request.method == 'POST':
        form = UpdateInformationForm(request.POST, request.FILES)
        if form.is_valid():
            room.capacity = form.cleaned_data['capacity']
            room.category = form.cleaned_data['capacity']
            room.description = form.cleaned_data['capacity']
            room.room_price = form.cleaned_data['room_price']
            room.room_picture = form.cleaned_data['room_picture']

            messages.success(request, "Room details were updated successfully!")
            return redirect("home")
    else:
        form = UpdateInformationForm()
    return render(request, 'room_form.html', {'form': form})


def room_detail(request, number):
    room = Room.objects.get(number=number)
    context = {'room': room}
    return render(request, 'room_detail.html', context)

def deleteRoom(request, number):
    room = Room.objects.get(number=number)
    room.delete()
    messages.success(request, "Room deleted successfully")
    return redirect("manage_room")

def profile_page(request):
    if(request.user.is_superuser):
        user = User.objects.get(id=request.user.id)
    else :
        user = UserProfile.objects.get(username=request.user.username)

    context = {'user' : user}
    return render(request, "profile_page_view.html", context)

def about(request):
    return render(request, "about.html")

def contact_us(request):
    return render(request, "contact_us.html")



def book_now(request, number, check_in, check_out):
    # Retrieve the room and booking details from the request
    room_number = request.GET.get('room_number')
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
    duration = (check_out_date - check_in_date).days

    # Create a Razorpay order with the amount and other details
    room = Room.objects.get(number=number)
    order_amount = (room.room_price * duration) # Replace with the actual amount
    print(order_amount)
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    razorpay_order = razorpay_client.order.create(dict(amount=(order_amount * 100), currency=order_currency, receipt=order_receipt, payment_capture=1))

    payment = Payment.objects.create(
    razorpay_order_id=razorpay_order['id'],
    amount=order_amount,
    currency=order_currency,
    user=request.user
    )
    # Render the payment form with the order details
    return render(request, 'payment_form.html', {'order_id': razorpay_order['id'], 'amount': order_amount, 'currency': order_currency, 'number' : number, 'check_in' : check_in, 'check_out' : check_out})

def success_payment_page(request, number, check_in, check_out):

    check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
    duration = (check_out_date - check_in_date).days
    roomDetail = Room.objects.get(number = number)
    amount = duration * roomDetail.room_price
    booking = Booking.objects.create(user=request.user, room=roomDetail, check_in=check_in_date, check_out=check_out_date)
    booking.save()
    bookinghistory = BookingHistory.objects.create()
    bookinghistory.id = booking.id
    bookinghistory.user = request.user
    bookinghistory.room = roomDetail
    bookinghistory.check_in = check_in
    bookinghistory.check_out = check_out
    bookinghistory.save()
    messages.success(request, "Payment Was Successfull")
    return redirect('generate_bill', booking_id=booking.id)

def generate_bill(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    duration = (booking.check_out - booking.check_in).days
    amount = booking.room.room_price * duration
    context = {'booking': booking, 'amount' : amount}
    return render(request, 'bill.html', context)

def active_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, "bookings.html", {'bookings' : bookings})

def booking_history(request):
    bookings = BookingHistory.objects.filter(user=request.user)
    return render(request, "bookinghistory.html", {'bookings' : bookings})

def cancel_booking(request, id):
    booking = Booking.objects.get(id=id)
    booking.delete()
    messages.success(request, "Booking Cancelled Successfully!")
    return redirect("active_bookings")

def removeHistory(request, id):
    bookinghistory = BookingHistory.objects.get(id = id)
    bookinghistory.delete()
    messages.success(request, "Removal from history successfull!")
    return redirect("booking_history")

def editprofile(request):
    if request.user.is_superuser :
        user = User.objects.get(id=request.user.id)
    else : 
        user = UserProfile.objects.get(id=request.user.id)
    if request.method == "POST":
        form = UserUpdateInformationForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mobile_number = form.cleaned_data['mobile_number']
            address = form.cleaned_data['address']
            profile_picture = form.cleaned_data['profile_picture']
            new_password = form.cleaned_data['new_password']
            email = form.cleaned_data['email']

            user.mobile_number = mobile_number=mobile_number
            user.address = address
            user.profile_picture = profile_picture
            user.password = new_password
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(request, "Information updated successfully." )
            return redirect("home")
        messages.error(request, "Unsuccessful.")
    form = UserUpdateInformationForm()
    return render (request=request, template_name="UpdateInformation.html", context={"register_form":form})

def show_all_rooms(request):
    Rooms = Room.objects.all()
    context = {'Rooms' : Rooms}
    return render(request, "show_all_rooms.html", context)

def imagegallery(request):
    images = ImageGallery.objects.all()
    context = {'images' : images}
    return render(request, "imagegallery.html", context)

def add_images(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            imagegallery = ImageGallery.objects.create(image=image)
            imagegallery.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect("manage_room")
    else:
        form = ImageForm()
    return render(request, 'room_form.html', {'form': form})

def delete_images(request):
    images = ImageGallery.objects.all()
    context = {'images' : images}
    return render(request, "image_deletion.html", context)

def delete_image_request(request, id):
    print(id)
    image = ImageGallery.objects.get(id=id)
    image.delete()
    messages.success(request, "Image deleted successfully")
    return redirect("imagegallery")

from django.db.models import Count, Sum
from django.shortcuts import render
from .models import Booking, Room, Payment

def generate_hotel_report(request):
    # Get total number of bookings
    num_bookings = Booking.objects.count()
    
    # Get total revenue generated
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total']
    
    # Get total number of rooms
    num_rooms = Room.objects.count()
    
    # Get total number of bookings for each room category
    bookings_by_category = Booking.objects.values('room__category').annotate(count=Count('id')).order_by('room__category')


    total_capacity = Room.objects.aggregate(total=Sum('capacity'))['total']
    avg_occupancy_rate = (num_bookings / total_capacity) * 100
    
    context = {
        'num_bookings': num_bookings,
        'total_revenue': total_revenue,
        'num_rooms': num_rooms,
        'bookings_by_category': bookings_by_category,
        'avg_occupancy_rate': avg_occupancy_rate,
    }
    
    return render(request, 'hotel_report.html', context)
