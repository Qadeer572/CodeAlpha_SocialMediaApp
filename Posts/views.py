from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from .models import Post, Comment, Followers, profile

# Create your views here.


def home(request):
    return render(request, 'Posts/home.html')

def Myprofile(request):
    profile_v= profile.objects.filter(user=request.user).first()  
    posts = Post.objects.filter(user=request.user)
    followers = Followers.objects.filter(user=request.user)
    following = Followers.objects.filter(follower=request.user)
    if request.user.is_authenticated:
        return render(request, 'core/profile.html', {
            'profile': profile_v,
            'posts': posts,
            'followers': followers.count(),
            'following': following.count(),
        })
    else:
        return HttpResponse("You are not logged in. Please log in to access this page.")


 