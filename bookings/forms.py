from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DarshanBooking, RoomBooking, DarshanSlot

class DarshanBookingForm(forms.ModelForm):
    class Meta:
        model = DarshanBooking
        fields = ['darshan_slot', 'booking_date', 'number_of_people', 'special_requirements']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'darshan_slot': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        temple = kwargs.pop('temple', None)
        super().__init__(*args, **kwargs)
        
        if temple:
            self.fields['darshan_slot'].queryset = DarshanSlot.objects.filter(
                temple=temple, is_active=True
            )

    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        if booking_date < timezone.now().date():
            raise ValidationError("Booking date cannot be in the past.")
        if booking_date > timezone.now().date() + timedelta(days=30):
            raise ValidationError("Booking date cannot be more than 30 days in advance.")
        return booking_date

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['check_in_date', 'check_out_date', 'number_of_guests', 'special_requests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data['check_in_date']
        if check_in_date < timezone.now().date():
            raise ValidationError("Check-in date cannot be in the past.")
        return check_in_date

    def clean_check_out_date(self):
        check_out_date = self.cleaned_data['check_out_date']
        check_in_date = self.cleaned_data.get('check_in_date')
        
        if check_in_date and check_out_date <= check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")
        
        return check_out_date