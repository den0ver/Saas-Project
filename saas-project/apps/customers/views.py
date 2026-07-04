from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateCustomerForm, EditCustomerForm
from .models import Customer
from apps.companies.models import Company
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.companies.utils import get_user_company


@login_required
def list_customers(request):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    customers = Customer.objects.filter(company=company)

    context = {'customers': customers}
    return render(request, 'customers/list.html', context)


@login_required
def create_customer(request):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    if request.method == "POST":
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.company = company
            customer.save()
            return redirect('customers:list')
    else:
        form = CreateCustomerForm()
    context = {'form': form}
    return render(request, 'customers/create.html', context)


@login_required
def detail_customer(request, id):
    company = get_user_company(request.user)
    
    if not company:
        return redirect('companies:create')

    customer = get_object_or_404(Customer, id=id, company=company)
    context = {'customer': customer}
    return render(request, 'customers/detail.html', context)


@login_required
def edit_customer(request, id):
    company = get_user_company(request.user)
    customer = get_object_or_404(Customer, id=id, company=company)

    if request.method == "POST":
        form = EditCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers:detail', id=customer.id)
    else:
        form = EditCustomerForm(instance=customer)
    context = {'form': form, 'customer': customer}
    return render(request, 'customers/edit.html', context)


@require_POST
@login_required
def delete_customer(request, id):
    company = get_user_company(request.user)
    customer = get_object_or_404(Customer, id=id, company=company)
    
    customer.delete()
    return redirect('customers:list')
