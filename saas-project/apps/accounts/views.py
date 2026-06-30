from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, RegisterForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from apps.companies.models import Company


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            context = {'new_user': new_user}
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                companies = Company.objects.filter(owner=user)
                if companies.count() == 0:
                    return redirect('companies:create')
                elif companies.count() == 1:
                    #messages.success(request, "Successfully authenticated!")
                    return redirect('dashboard:dashboard')
                else:
                    return redirect('companies:list')
            else:
                pass
                #messages.error(request, "Invalid login.")
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

@login_required
@require_POST
def user_logout(request):
    logout(request)
    return redirect('accounts:login')
