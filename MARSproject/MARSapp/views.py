from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'base_generic.html', )

def hmarlanding(request):
    return render(request, 'hmartest.html')