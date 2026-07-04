from django.shortcuts import render, redirect
from .models import Service
from apps.companies.utils import get_user_company
from .forms import CreateServiceForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify


@login_required
def list_services(request):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    services = Service.objects.filter(company=company)
    form = CreateServiceForm()

    context = {'form': form, 'services': services}
    return render(request, 'services/list.html', context)


@login_required
def create_service(request):
    company = get_user_company(request.user)

    if not company:
        return redirect('companies:create')

    if request.method == "POST":
        form = CreateServiceForm(request.POST)

        if form.is_valid():
            service = form.save(commit=False)
            service.company = company
            service.slug = slugify(service.name)
            service.save()
            return redirect('services:list_services')
    else:
        form = CreateServiceForm()
    context = {'form': form}
    return render(request, 'services/create.html', context)

