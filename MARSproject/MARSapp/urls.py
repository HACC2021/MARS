from django.urls import path
from . import views
from django.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('formselect/', views.formselect, name='formselect'),
    path('emergency/', views.emergency, name='emergency'),
    path("login/", views.login, name='login'),

    #accessing each form from pickform
    path('sealreport/', views.sealreport, name='sealreport'),
    path('birdreport/', views.birdreport, name='birdreport'),
    path('turtlereport/', views.turtlereport, name='turtlereport'),

    path('hmar/', views.hmar, name='hmar'),


    path('sealsubmit/', views.sealsubmit, name='sealsubmit'),
    path('birdsubmit/', views.birdsubmit, name='birdsubmit'),
    path('turtlesubmit/', views.turtlesubmit, name='turtlesubmit'),

    path('hmar/<str:ID>/', views.specificreport, name='exportdata'),
    path('hmar/<str:ID>', views.specificreport, name='specificreport'),
    path('hmar/<str:ID>/editform/', views.editform, name='editform'),

    #create edit thank you page that has button to redirect to home
    path('hmar/<str:ID>/editform/editsubmit/', views.editredirect, name='editredirect'),
]
