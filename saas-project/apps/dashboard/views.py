from django.shortcuts import render, redirect
from apps.companies.models import Company
from apps.services.models import Service
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    company = Company.objects.filter(owner=request.user).first()

    if not company:
        return redirect('companies:create')
    
    services_count = Service.objects.filter(company=company).count()
    
    stats = {
        'bookings_today': 0,
        'bookings_pending': 0,
        'revenue': '$ 0',
        'total_customers': 0,
        'tasks_open': 0,
        'services_count': services_count,
    }

    context = {
        'company': company,
        'stats': stats,
        'recent_bookings': [],
        'todays_bookings': [],
        'open_tasks': [],
        'top_services': [],
        'employees_load': [],
    }

    return render(request, 'dashboard/dashboard.html', context)
