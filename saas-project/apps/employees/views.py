from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from apps.companies.models import Company
from apps.companies.utils import get_user_company
from .forms import CreateEmployeeForm, EditEmployeeForm
from django.contrib.auth.decorators import login_required


@login_required
def list_employees(request):
    company = Company.objects.filter(owner=request.user).first()

    if not company:
        return redirect('companies:create')

    employees = Employee.objects.filter(company=company)
    context = {'employees': employees}
    return render(request, 'employees/list.html', context)


@login_required
def create_employee(request):
    company = Company.objects.filter(owner=request.user).first()

    if not company:
        return redirect('companies:create')

    if request.method == "POST":
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = company
            employee.save()
            return redirect('employees:list')
    else:
        form = CreateEmployeeForm()
    context = {'form': form}
    return render(request, 'employees/create.html', context)


@login_required
def detail_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    context = {'employee': employee}
    return render(request, 'employees/detail.html', context)


@login_required
def edit_employee(request, id):
    company = get_user_company(user=request.user)
    employee = get_object_or_404(Employee, id=id, company=company)
    if request.method == "POST":
        form = EditEmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:detail', id=employee.id)
    else:
        form = EditEmployeeForm(instance=employee)
    context = {'form': form, 'employee': employee}
    return render(request, 'employees/edit.html', context)


@login_required
def delete_employee(request, id):
    company = get_user_company(user=request.user)
    employee = get_object_or_404(Employee, id=id, company=company)
    employee.delete()
    return redirect('employees:list')