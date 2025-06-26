from django.contrib import admin
from .models import Temple, DarshanSlot, DarshanBooking, Room, RoomBooking

@admin.register(Temple)
class TempleAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'darshan_price', 'is_active', 'created_at']
    list_filter = ['is_active', 'location', 'created_at']
    search_fields = ['name', 'location']
    list_editable = ['is_active']

@admin.register(DarshanSlot)
class DarshanSlotAdmin(admin.ModelAdmin):
    list_display = ['temple', 'slot_type', 'start_time', 'end_time', 'max_capacity', 'price', 'is_active']
    list_filter = ['temple', 'slot_type', 'is_active']
    list_editable = ['is_active']

@admin.register(DarshanBooking)
class DarshanBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'temple', 'booking_date', 'number_of_people', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'temple', 'booking_date', 'created_at']
    search_fields = ['booking_id', 'user__username', 'temple__name']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['temple', 'room_number', 'room_type', 'capacity', 'price_per_night', 'is_available']
    list_filter = ['temple', 'room_type', 'is_available']
    search_fields = ['room_number', 'temple__name']
    list_editable = ['is_available']

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'room', 'check_in_date', 'check_out_date', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'room__temple', 'check_in_date', 'created_at']
    search_fields = ['booking_id', 'user__username', 'room__temple__name']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']