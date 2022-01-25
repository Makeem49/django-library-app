from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('Hello wolrd, this is my first django web application.')

def about(request):
    return HttpResponse('About page')

def faq(request):
    return HttpResponse('Frequestly asked question page')
