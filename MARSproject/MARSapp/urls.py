from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    #path('hmar/', views.hmar, name='hmar'),
    path('emergency/', views.emergency, name = 'emergency'),
    path("login/", views.login, name = 'login'),
    path('sighting/', views.sighting, name = 'sighting'),



]
