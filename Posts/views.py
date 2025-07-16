from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from .models import Post, Comment, Followers, profile

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        posts=[]
        following_post=[]
        following = Post.objects.filter(user__in=Followers.objects.filter(follower=request.user).values_list('user', flat=True)).order_by('-created_at')
        for post in following:
            profile_v = profile.objects.filter(user=post.user).first()
            following_post.append({
                'post': post,
                'profile': profile_v,
            })
        post_list= Post.objects.exclude(user=request.user).order_by('-created_at')
        for post1 in post_list:
            profile_v = profile.objects.filter(user=post1.user).first()
            posts.append({
                'post': post1,
                'profile': profile_v,
            })
        comments = Comment.objects.all()
        return render(request, 'Posts/home.html',{
            'foryou_posts': posts,
            'following_posts':following_post,
            'comments': comments,
        })
    else:
        return render(request, 'Posts/home.html')

def Myprofile(request):
    profile_v= profile.objects.filter(user=request.user).first()  
    posts = Post.objects.filter(user=request.user)
    followers = Followers.objects.filter(user=request.user)
    following = Followers.objects.filter(follower=request.user)
    No_Follower=followers.count()
    No_Following=following.count()
    if request.user.is_authenticated:
        return render(request, 'core/profile.html', {
            'profile': profile_v,
            'posts': posts,
            'followers': followers.count(),
            'following': following.count(),
        })
    else:
        return HttpResponse("You are not logged in. Please log in to access this page.")

def ulploadPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.method == 'POST':
                content = request.POST.get('content')
                post_type = request.POST.get('type')
                media = request.FILES.get('media') if post_type in ['image', 'video'] else None

                Post.objects.create(
                    user=request.user,
                    content=content,
                    type=post_type,
                    media=media
                )
                return redirect('/profile/')
        return render(request, 'Posts/uploadPost.html')
    else:
        return HttpResponse("You are not logged in. Please log in to access this page.")
    
 