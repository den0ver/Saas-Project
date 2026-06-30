from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'is_active', 'created']
    list_display_links = ['id', 'name']
    list_filter = ['name']
