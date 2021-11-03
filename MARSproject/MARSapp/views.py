from django.shortcuts import render
from .forms import formdata
from .models import formdata
# Create your views here.

def home(request):
    return render(request, 'home.html', )
'''
def hmar(request):
    return render(request, 'hmar.html')
'''

def emergency(request):
    return render(request, 'emergency.html')

def login(request):
    return render(request, 'login.html')

def sighting(request):
    return render(request, 'sighting.html')



