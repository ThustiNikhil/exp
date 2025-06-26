from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Temple(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='temples/', blank=True, null=True)
    darshan_price = models.DecimalField(max_digits=10, decimal_places=2)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class DarshanSlot(models.Model):
    SLOT_CHOICES = [
        ('morning', 'Morning (6:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:00 PM - 6:00 PM)'),
        ('evening', 'Evening (6:00 PM - 10:00 PM)'),
    ]
    
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='darshan_slots')
    slot_type = models.CharField(max_length=20, choices=SLOT_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_capacity = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.temple.name} - {self.get_slot_type_display()}"

    class Meta:
        unique_together = ['temple', 'slot_type']

class DarshanBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE)
    darshan_slot = models.ForeignKey(DarshanSlot, on_delete=models.CASCADE)
    booking_date = models.DateField()
    number_of_people = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_id = models.CharField(max_length=20, unique=True)
    special_requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_id} - {self.user.username} - {self.temple.name}"

    class Meta:
        ordering = ['-created_at']

class Room(models.Model):
    ROOM_TYPES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Suite'),
        ('dormitory', 'Dormitory'),
    ]

    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField(help_text="Comma-separated list of amenities")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.temple.name} - Room {self.room_number} ({self.get_room_type_display()})"

    class Meta:
        unique_together = ['temple', 'room_number']

class RoomBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_id = models.CharField(max_length=20, unique=True)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_id} - {self.user.username} - {self.room}"

    def get_total_nights(self):
        return (self.check_out_date - self.check_in_date).days

    class Meta:
        ordering = ['-created_at']