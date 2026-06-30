# forms.py
from django import forms
from .models import Company

class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']
        labels = {
            'name': 'Название компании',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Например: Барбершоп «Чёрный квадрат»',
                'autocomplete': 'organization',
                'autofocus': True,
            }),
        }
        error_messages = {
            'name': {
                'required': 'Укажите название компании',
                'max_length': 'Название слишком длинное',
            }
        }