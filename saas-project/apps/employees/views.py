from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from apps.companies.models import Company
from .forms import CreateEmployeeForm
from django.contrib.auth.decorators import login_required


@login_required
def list_employees(request):
    company = Company.objects.filter(owner=request.user).first()
    employees = Employee.objects.filter(company=company)
    context = {'employees': employees}
    return render(request, 'employees/list.html', context)


@login_required
def create_employee(request):
    company = Company.objects.filter(owner=request.user).first()
    if request.method == "POST":
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = company
            employee.save()
            return redirect('employees:list_employees')
    else:
        form = CreateEmployeeForm()
    context = {'form': form}
    return render(request, 'employees/create.html', context)


@login_required
def detail_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    context = {'employee': employee}
    return render(request, 'employees/detail.html', context)