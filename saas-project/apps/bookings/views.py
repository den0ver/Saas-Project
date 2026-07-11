from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import CreateBookingForm, EditBookingForm
from .models import Booking
from apps.companies.models import Company
from apps.services.models import Service
from apps.employees.models import Employee
from apps.customers.models import Customer
from apps.companies.utils import get_user_company
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import timedelta, datetime
from django.utils import timezone


@login_required
def list_bookings(request):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    bookings = Booking.objects.filter(company=company)
    context = {'bookings': bookings}
    return render(request, 'bookings/list.html', context)


@login_required
def create_booking(request):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    if request.method == "POST":
        form = CreateBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.company = company
            booking.save()
            return redirect('bookings:list')
    else:
        form = CreateBookingForm()
    context = {'form': form, 'company': company}
    return render(request, 'bookings/create.html', context)


@login_required
def detail_booking(request, id):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    booking = get_object_or_404(Booking, id=id, company=company)
    context = {'booking': booking}
    return render(request, 'bookings/detail.html', context)


@login_required
def edit_booking(request, id):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    booking = get_object_or_404(Booking, id=id, company=company)

    if request.method == "POST":
        form = EditBookingForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('bookings:detail', id=booking.id)
    else:
        form = EditBookingForm(instance=booking)
    context = {'form': form, 'booking': booking}
    return render(request, 'bookings/edit.html', context)


@login_required
@require_POST
def delete_booking(request, id):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    booking = get_object_or_404(Booking, id=id, company=company)
    booking.delete()
    return redirect('bookings:list')


def _calculate_slots(employee, service, selected_date):
    """Считает доступные слоты 9:00-18:00 с шагом 30 минут для конкретного сотрудника/услуги/даты."""
    if not (employee and service):
        return []

    slot = timezone.make_aware(datetime.combine(selected_date, datetime.min.time()).replace(hour=9))
    end = timezone.make_aware(datetime.combine(selected_date, datetime.min.time()).replace(hour=18))
    duration = timedelta(minutes=service.duration)

    slots = []
    while slot + duration <= end:
        busy = Booking.objects.filter(
            employee=employee, start_time__lt=slot + duration, end_time__gt=slot
        ).exists()
        slots.append({'iso': slot.isoformat(), 'label': slot.strftime('%H:%M'), 'disabled': busy})
        slot += timedelta(minutes=30)

    return slots


def get_slots(request, company_slug):
    """AJAX-эндпоинт: отдаёт JSON со слотами на выбранную дату/услугу/специалиста без перезагрузки страницы."""
    company = get_object_or_404(Company, slug=company_slug)

    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'slots': []})

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'slots': []})

    employee_id = request.GET.get('employee')
    service_id = request.GET.get('service')

    employee = (
        Employee.objects.filter(company=company, id=employee_id).first()
        if employee_id else Employee.objects.filter(company=company).first()
    )
    service = Service.objects.filter(company=company, id=service_id).first() if service_id else None

    slots = _calculate_slots(employee, service, selected_date)
    return JsonResponse({'slots': slots})


def public_booking(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    services = Service.objects.filter(company=company)
    employees = Employee.objects.filter(company=company)

    today = timezone.localdate()
    available_days = [{'date': today + timedelta(days=i)} for i in range(14)]

    selected_date = today
    if request.GET.get('date'):
        selected_date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()

    employee_id = request.GET.get('employee')
    service_id = request.GET.get('service')

    employee = Employee.objects.filter(id=employee_id).first() if employee_id else employees.first()
    service = Service.objects.filter(id=service_id).first() if service_id else None

    available_slots = _calculate_slots(employee, service, selected_date)

    if request.method == "POST":
        form = CreateBookingForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            employee = form.cleaned_data['employee']
            start_time = form.cleaned_data['start_time']
            end_time = start_time + timedelta(minutes=service.duration)

            # Если специалист не выбран ("Без разницы") — ищем первого свободного на это время
            if not employee:
                employee = Employee.objects.filter(company=company).exclude(
                    bookings__start_time__lt=end_time,
                    bookings__end_time__gt=start_time
                ).first()

            # Без сотрудника дальше не идём — иначе IntegrityError
            if not employee:
                context = {
                    'form': form, 'company': company, 'error': 'На это время нет свободных специалистов',
                    'services': services, 'employees': employees,
                    'available_days': available_days, 'available_slots': available_slots,
                    'selected_date': selected_date,
                    'selected_service_id': service_id or '',
                    'selected_employee_id': employee_id or '',
                }
                return render(request, 'bookings/public_booking.html', context)

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')

            customer, created = Customer.objects.get_or_create(company=company, phone=phone, defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })

            customer.first_name = first_name
            customer.last_name = last_name
            customer.email = email
            customer.save()

            exists = Booking.objects.filter(employee=employee, start_time__lt=end_time, end_time__gt=start_time).exists()

            if exists:
                context = {
                    'form': form, 'company': company, 'error': 'This time is already booked',
                    'services': services, 'employees': employees,
                    'available_days': available_days, 'available_slots': available_slots,
                    'selected_date': selected_date,
                    'selected_service_id': service_id or '',
                    'selected_employee_id': employee_id or '',
                }
                return render(request, 'bookings/public_booking.html', context)

            Booking.objects.create(company=company, service=service, employee=employee, customer=customer,
            start_time=start_time, end_time=end_time)

            return redirect('bookings:created')
    else:
        form = CreateBookingForm()

    context = {
        'form': form, 'company': company, 'services': services, 'employees': employees,
        'available_days': available_days, 'available_slots': available_slots,
        'selected_date': selected_date,
        'selected_service_id': request.GET.get('service', ''),
        'selected_employee_id': request.GET.get('employee', ''),
    }
    return render(request, 'bookings/public_booking.html', context)


def created_booking(request):
    return render(request, 'bookings/created.html')