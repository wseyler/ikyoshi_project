from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.contrib import messages


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


@require_http_methods(["GET", "POST"])
def signupuser(request):
    """Optimized signup view using Django forms properly"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('home')
            except IntegrityError:
                form.add_error('username', 'That username has already been taken. Please choose a new username.')
        # Form is invalid or IntegrityError occurred
        return render(request, 'pages/signupuser.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'pages/signupuser.html', {'form': form})


@require_http_methods(["POST"])
def logoutuser(request):
    """Optimized logout view - POST only"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@require_http_methods(["GET", "POST"])
def loginuser(request):
    """Optimized login view using Django forms properly"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                if user.is_superuser:
                    return redirect('admin:index')
                return redirect('home')
        # Invalid credentials
        messages.error(request, 'Username and password did not match.')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/loginuser.html', {'form': form})
