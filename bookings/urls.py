from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('temples/', views.temple_list, name='temple_list'),
    path('temples/<int:temple_id>/', views.temple_detail, name='temple_detail'),
    path('temples/<int:temple_id>/book-darshan/', views.book_darshan, name='book_darshan'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('booking-confirmation/<str:booking_type>/<str:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]