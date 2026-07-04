from django import forms
from .models import Booking


class CreateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'employee', 'customer', 'date', 'time', 'status']


class EditBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'employee', 'customer', 'date', 'time', 'status']