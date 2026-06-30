from django.shortcuts import render
from .models import Service
from .forms import CreateServiceForm


def create_service(request):
    if request.method == "POST":
        form = CreateServiceForm(request.POST)
    else:
        form = CreateServiceForm()
    context = {'form': form}
    return render(request, '', context)
