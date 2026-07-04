from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBookingForm, EditBookingForm
from .models import Booking
from apps.companies.utils import get_user_company
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


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