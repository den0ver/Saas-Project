from django.shortcuts import render, redirect
from .forms import CompanyCreateForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required


@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.slug = slugify(company.name)
            company.save()
            return redirect('dashboard:dashboard')
    else:
        form = CompanyCreateForm()
    context = {'form': form}
    return render(request, 'companies/create.html', context)
