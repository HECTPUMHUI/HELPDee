from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'task/index.html')


def about(request):
    return render(request, 'task/about.html')


def degrees(request, degid):
    return HttpResponse(f'<h1>Degrees</h1><p>{degid}</p>')
