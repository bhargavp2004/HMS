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

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)