from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'service', 'employee', 'customer']
    list_display_links = ['id', 'company']
