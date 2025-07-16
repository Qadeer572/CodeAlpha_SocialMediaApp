from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.home, name='home'),  # Login view
    path('profile/', views.Myprofile, name='profile'),  # Home view
]

 