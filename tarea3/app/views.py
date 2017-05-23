from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse(render(request, 'app/index.html', {}))


def login(request):
    return HttpResponse(render(request, 'app/login.html', {}))


def signup(request):
    return HttpResponse(render(request, 'app/signup.html', {}))
