from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),  # Login view
    path('profile/', views.Myprofile, name='profile'),  # Home view
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 