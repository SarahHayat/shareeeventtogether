from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def djangorocks (request):
    name = 'sarah'
    body= 'je mapelle {}'.format(name)
    return HttpResponse(body)