from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='home'),

    path('emergency/', views.emergency, name = 'emergency'),
    path("login/", views.login, name = 'login'),
    path('sighting/', views.sighting, name = 'sighting'),
    path('hmar/', views.hmar, name='hmar'),
    path('editform/', views.editform, name = 'editform'),
    path('submitform/', views.submitform, name = 'submitform'),
    path('hmar/<str:ID>', views.specificreport, name = 'specific-report'),
]
