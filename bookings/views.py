from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import uuid
from .models import Temple, DarshanSlot, DarshanBooking, Room, RoomBooking
from .forms import DarshanBookingForm, RoomBookingForm

def home(request):
    temples = Temple.objects.filter(is_active=True)[:6]
    featured_rooms = Room.objects.filter(is_available=True)[:4]
    context = {
        'temples': temples,
        'featured_rooms': featured_rooms,
    }
    return render(request, 'bookings/home.html', context)

def temple_list(request):
    temples = Temple.objects.filter(is_active=True)
    search_query = request.GET.get('search')
    location_filter = request.GET.get('location')
    
    if search_query:
        temples = temples.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if location_filter:
        temples = temples.filter(location__icontains=location_filter)
    
    paginator = Paginator(temples, 9)
    page_number = request.GET.get('page')
    temples = paginator.get_page(page_number)
    
    locations = Temple.objects.values_list('location', flat=True).distinct()
    
    context = {
        'temples': temples,
        'locations': locations,
        'search_query': search_query,
        'location_filter': location_filter,
    }
    return render(request, 'bookings/temple_list.html', context)

def temple_detail(request, temple_id):
    temple = get_object_or_404(Temple, id=temple_id, is_active=True)
    darshan_slots = temple.darshan_slots.filter(is_active=True)
    rooms = temple.rooms.filter(is_available=True)
    
    context = {
        'temple': temple,
        'darshan_slots': darshan_slots,
        'rooms': rooms,
    }
    return render(request, 'bookings/temple_detail.html', context)

@login_required
def book_darshan(request, temple_id):
    temple = get_object_or_404(Temple, id=temple_id, is_active=True)
    
    if request.method == 'POST':
        form = DarshanBookingForm(request.POST, temple=temple)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.temple = temple
            booking.booking_id = f"D{uuid.uuid4().hex[:8].upper()}"
            booking.total_amount = booking.darshan_slot.price * booking.number_of_people
            booking.save()
            
            messages.success(request, f'Darshan booking confirmed! Your booking ID is {booking.booking_id}')
            return redirect('booking_confirmation', booking_type='darshan', booking_id=booking.booking_id)
    else:
        form = DarshanBookingForm(temple=temple)
    
    context = {
        'form': form,
        'temple': temple,
    }
    return render(request, 'bookings/book_darshan.html', context)

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)
    
    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.booking_id = f"R{uuid.uuid4().hex[:8].upper()}"
            
            # Calculate total amount
            nights = (booking.check_out_date - booking.check_in_date).days
            booking.total_amount = room.price_per_night * nights
            booking.save()
            
            messages.success(request, f'Room booking confirmed! Your booking ID is {booking.booking_id}')
            return redirect('booking_confirmation', booking_type='room', booking_id=booking.booking_id)
    else:
        form = RoomBookingForm()
    
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'bookings/book_room.html', context)

def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    temple_filter = request.GET.get('temple')
    room_type_filter = request.GET.get('room_type')
    
    if temple_filter:
        rooms = rooms.filter(temple_id=temple_filter)
    
    if room_type_filter:
        rooms = rooms.filter(room_type=room_type_filter)
    
    paginator = Paginator(rooms, 12)
    page_number = request.GET.get('page')
    rooms = paginator.get_page(page_number)
    
    temples = Temple.objects.filter(is_active=True)
    room_types = Room.ROOM_TYPES
    
    context = {
        'rooms': rooms,
        'temples': temples,
        'room_types': room_types,
        'temple_filter': temple_filter,
        'room_type_filter': room_type_filter,
    }
    return render(request, 'bookings/room_list.html', context)

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    context = {'room': room}
    return render(request, 'bookings/room_detail.html', context)

@login_required
def booking_confirmation(request, booking_type, booking_id):
    if booking_type == 'darshan':
        booking = get_object_or_404(DarshanBooking, booking_id=booking_id, user=request.user)
    else:
        booking = get_object_or_404(RoomBooking, booking_id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
        'booking_type': booking_type,
    }
    return render(request, 'bookings/booking_confirmation.html', context)

@login_required
def my_bookings(request):
    darshan_bookings = DarshanBooking.objects.filter(user=request.user)
    room_bookings = RoomBooking.objects.filter(user=request.user)
    
    context = {
        'darshan_bookings': darshan_bookings,
        'room_bookings': room_bookings,
    }
    return render(request, 'bookings/my_bookings.html', context)