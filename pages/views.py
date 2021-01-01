from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Permission
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'pages/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], '', request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home') #success, take me home!

            except IntegrityError:
                return render(request, 'pages/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'pages/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'pages/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'pages/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match' })
        else:
            login(request, user)
            if (user.is_superuser):
                return redirect('/admin') #success, take me home!
            else:
                return redirect('home') #success, take me home!
