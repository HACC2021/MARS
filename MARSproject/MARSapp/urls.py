from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.userlanding, name='userlanding'),
    path('hmar/', views.hmarlanding, name='hmarlanding'),
    path('emergency/', views.emergency, name = 'emergencyland'),
    path("loginpage/", views.loginpage, name = 'login'),
    path('basicpage/', views.basicpage, name = 'form')

]
