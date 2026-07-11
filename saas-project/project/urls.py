from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('companies/', include('apps.companies.urls')),
    path('crm/', include('apps.crm.urls')),
    path('services/', include('apps.services.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('employees/', include('apps.employees.urls')),
    path('api/', include('apps.api.urls')),
    path('customers/', include('apps.customers.urls')),
]
