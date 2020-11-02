from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def djangorocks (request):
    name = 'sarah'
    body= f'je mapelle {name}'
    return HttpResponse(body)