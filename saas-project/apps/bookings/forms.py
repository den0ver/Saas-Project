from django import forms
from .models import Booking
from apps.employees.models import Employee


class CreateBookingForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False,
    empty_label=None)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    class Meta:
        model = Booking
        fields = ['service', 'employee', 'start_time']


class EditBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'employee', 'customer', 'start_time', 'status']