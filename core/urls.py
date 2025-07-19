from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('editProfile/',views.editProfile, name='editProfile'),  
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard view 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 