from django import forms
from .models import Employee


class CreateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone', 'email', 'is_active']


class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone', 'email', 'is_active']