from django.contrib import admin
from django.urls import path, include
from HMS_APP import views
from HMS_APP.views import RoomList, BookingList, BookingView, register_request
from django.conf import settings
from django.conf.urls.static import static
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
    path('room_detail/<number>', views.room_detail, name = 'room_detail'),
    path('create_room', views.create_room, name = 'create_room'),
    path('manage_room/', views.manage_room, name = "manage_room"),
    path('deletion_list_view', views.delete_room, name = "delete_room"),
    path('deleteRoom/<number>/', views.deleteRoom, name = "deleteRoom"),
    path('profile_page/', views.profile_page, name = "profile_page"),
    path('about/', views.about, name="about"),
    path('contact_us/', views.contact_us, name = "contact_us"),
    path('book_room_now/<number>/<check_in>/<check_out>', views.book_now, name="book_now"),
    path('success_payment_page/<number>/<check_in>/<check_out>', views.success_payment_page, name = "success_payment_page"),
    path('generate_bill/<booking_id>', views.generate_bill, name = "generate_bill"),
    path('update_room/', views.update_room, name = "update_room"),
    path('update_request/<number>', views.update_request, name = "update_request"),
    path('active_bookings/', views.active_bookings, name = "active_bookings"),
    path('booking_history/', views.booking_history, name = "booking_history"),
    path('cancel_booking/<id>', views.cancel_booking, name = "cancel_booking"),
    path('removeHistory/<id>', views.removeHistory, name = "removeHistory"),
    path('show_all_rooms/', views.show_all_rooms, name = "show_all_rooms"),
    path('imagegallery/', views.imagegallery, name="imagegallery"),
    path('add_images/', views.add_images, name = "add_images"),
    path('delete_images/', views.delete_images, name = "delete_images"),
    path('delete_image_request/<id>/', views.delete_image_request, name = "delete_image_request"),
    # path('editprofile/', views.editprofile, name = "edit_profile"),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
