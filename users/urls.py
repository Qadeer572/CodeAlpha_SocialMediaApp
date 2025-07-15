from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('login/',views.loginView, name='login'),  # Login view
    path('logout/', views.logout, name='logout'),  # Logout view
    path('login_api/', views.login.as_view(), name='login_api'),  # API login view
]

 