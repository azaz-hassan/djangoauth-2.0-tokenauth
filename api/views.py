from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def homepage(request):
    return HttpResponse("Hello World")

