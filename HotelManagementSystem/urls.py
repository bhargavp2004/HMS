"""HotelManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from HMS_APP import views
from HMS_APP.views import RoomList, BookingList, BookingView, register_request
app_name = "HMS_APP"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('room_list/', RoomList.as_view(), name = "roomlist"),
    path('booking_list/', BookingList.as_view(), name = "bookinglist"),
    path('book_now/', views.showDetails, name = "showDetails"),
    path('BookSelection/<number>/<check_in>/<check_out>', views.BookSelection, name = "BookSelection"),
    path('book/', BookingView.as_view(), name = 'booking_view'),
    path('register/', views.register_request, name = "register"),
    path('login/', views.login_request, name = "login"),
    path('logout/', views.logout_request, name = "logout"),
    path('room_search_view/', views.room_search_view, name = "room_search_view"),
]


#no need to make changes
