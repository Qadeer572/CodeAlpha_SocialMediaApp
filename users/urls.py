from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('login/',views.login_view, name='login'),  # Login view
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('suggestedAccount/', views.suggestedAccount, name='suggestedAccount'),  # Suggested accounts view
]

 