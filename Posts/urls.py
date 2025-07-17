from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from Posts.views import likePost,followUser

urlpatterns = [
    path('',views.home, name='home'),  # Login view
    path('profile/', views.Myprofile, name='profile'),  # Home view
    path('uploadPost/', views.uploadPost, name='uploadPost'),  # Edit profile view
    path('likePost/',likePost.as_view(), name='likePost'),  # Like post view
    path('follow/', views.followUser.as_view(), name='follow'),  # Follow user view
    path('followingList/', views.followingList, name='followingList'),  # Following list view
    path('followersList/', views.followersList, name='followersList'),  # Followers list view
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 