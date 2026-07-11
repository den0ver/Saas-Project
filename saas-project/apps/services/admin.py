from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'name', 'price', 'duration', 'is_active']
    list_display_links = ['id', 'name']
