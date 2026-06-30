from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display = ['id', 'company', 'first_name', 'last_name', 'email', 'phone']
    list_display_links = ['id', 'company']
    list_filter = ['first_name', 'last_name', 'company']
