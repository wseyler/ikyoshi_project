from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Hello, from the People index.</h1>")
