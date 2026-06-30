from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'company']
    list_display_links = ['id', 'first_name', 'last_name']
    list_filter = ['first_name', 'last_name']
