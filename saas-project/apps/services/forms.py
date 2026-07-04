from django import forms
from .models import Service


class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'time', 'price', 'description', 'is_active']
