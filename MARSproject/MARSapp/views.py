from django.shortcuts import render

# Create your views here.

def userlanding(request):
    return render(request, 'userlanding.html', )

def hmarlanding(request):
    return render(request, 'hmartest.html')

#def userlanding(request):
    #return render(request, 'userlanding.html')

def emergency(request):
    return render(request, 'emergencyland.html')

def loginpage(request):
    return render(request, 'loginpage.html')

def basicpage(request):
    return render(request, 'form.html')

