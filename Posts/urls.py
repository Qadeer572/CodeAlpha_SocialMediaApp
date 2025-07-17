from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from Posts.views import likePost

urlpatterns = [
    path('',views.home, name='home'),  # Login view
    path('profile/', views.Myprofile, name='profile'),  # Home view
    path('uploadPost/', views.ulploadPost, name='uploadPost'),  # Edit profile view
    path('likePost/',likePost.as_view(), name='likePost'),  # Like post view
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 