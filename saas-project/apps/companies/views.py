from django.shortcuts import render, redirect
from .forms import CompanyCreateForm
from django.utils.text import slugify
from .models import Company
from django.contrib.auth.decorators import login_required


@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user

            base_slug = slugify(company.name)
            slug = base_slug
            counter = 1

            while Company.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            company.slug = slug
            company.save()

            return redirect('dashboard:dashboard')
    else:
        form = CompanyCreateForm()
    context = {'form': form}
    return render(request, 'companies/create.html', context)
