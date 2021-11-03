from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('emergency/', views.emergency, name = 'emergency'),
    path('login/', views.login, name = 'login'),
    path('sighting/', views.sighting, name = 'sighting'),
    path('hmar/', views.hmar, name='hmar'),
    #path('<hmar/int:ticketnum>/', views.report, name = 'report')
]
