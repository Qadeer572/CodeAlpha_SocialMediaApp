from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from .models import Post, Comment, Followers, profile
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from users.forms import UserLoginForm

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        posts=[]
        following_post=[]
        following = Post.objects.filter(user__in=Followers.objects.filter(follower=request.user).values_list('user', flat=True)).order_by('-created_at')
        for post in following:
            profile_v = profile.objects.filter(user=post.user).first()
            liked = post.likes.filter(id=request.user.id).exists()
            comments = Comment.objects.filter(post=post).order_by('-created_at')
            following_post.append({
                'post': post,
                'profile': profile_v,
                'liked': liked,
                'comments':comments,
            })

        post_list= Post.objects.exclude(user=request.user).order_by('-created_at')
        for post1 in post_list:
            profile_v = profile.objects.filter(user=post1.user).first()
            liked = post1.likes.filter(id=request.user.id).exists()
            comments1 = Comment.objects.filter(post=post1).order_by('-created_at')
            posts.append({
                'post': post1,
                'profile': profile_v,
                'liked': liked,
                'comments':comments1,
            })
        
        following_list = User.objects.filter(following__follower=request.user)
        return render(request, 'Posts/home.html',{
            'foryou_posts': posts,
            'following_posts':following_post,
            'following_list': following_list,
        })
    else:
        form=UserLoginForm()
        return render(request, 'users/login.html',{'form': form})

def Myprofile(request):
    profile_v= profile.objects.filter(user=request.user).first()  
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
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
def followersList(request):
    if request.user.is_authenticated:
        followers = Followers.objects.filter(user=request.user)
        follower_users = [f.follower for f in followers]
        profiles = profile.objects.filter(user__in=follower_users)
        following= Followers.objects.filter(follower=request.user)
        return render(request, 'Posts/followerList.html', {'profiles': profiles, 'following': following})
    else:
        return HttpResponse("You are not logged in. Please log in to access this page.")
def followingList(request):
    if request.user.is_authenticated:
        following = Followers.objects.filter(follower=request.user)
        following_users = [f.user for f in following]
        profiles1 = profile.objects.filter(user__in=following_users)
        profiles=[]
        for profile1 in profiles1:
            if profile1.user != request.user:
                profiles.append({
                    "profile":profile1,
                    "TotalFollower": Followers.objects.filter(user=profile1.user).count(),
                    })
        return render(request, 'Posts/followingList.html', {'profiles': profiles})
    else:
        return HttpResponse("You are not logged in. Please log in to access this page.")
def uploadPost(request):
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
    


class likePost(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        try:
            post_id = request.data.get('id')
            post = Post.objects.get(id=post_id)

            if request.user in post.likes.all():
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user)
                liked = True

            likes_count = post.likes.count()
            
            return Response({  # Use capital R here
                "status": True,
                "liked": liked,
                "likes_count": likes_count,
            })

        except Post.DoesNotExist:
            return HttpResponse(status=404)


class followUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.data.get('id')
            user_to_follow = User.objects.get(id=user_id)

            if user_to_follow == request.user:
                return Response({"status": False, "message": "You cannot follow yourself."})

            follow_instance, created = Followers.objects.get_or_create(user=user_to_follow, follower=request.user)
            is_following=False
            if created:
                is_following = True
                return Response({
                    "status": True,
                    "is_following": is_following,
                    "message": "You are now following this user."
                    })
            else:
                follow_instance.delete()
                return Response({
                        "status": True,
                        "is_following": is_following,
                        "message": "You have unfollowed this user."
                        })

        except User.DoesNotExist:
            return HttpResponse(status=404)        

 

class add_comment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            post_id = request.data.get('postId')
            content = request.data.get('content')

            # Validate input
            if not post_id or not content:
                return Response({
                    "status": False,
                    "message": "postId and content are required."
                }, status=status.HTTP_400_BAD_REQUEST)

            post = Post.objects.get(id=post_id)

            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

            profile1 = profile.objects.filter(user=request.user).first()

            return Response({
                "status": True,
                "message": "Comment added successfully.",
                "comment": {
                    "id": comment.id,
                    "profile_pic": profile1.profile_picture.url if profile1 and profile1.profile_picture else None,
                    "username": comment.user.username,
                    "user_id": comment.user.id,
                    "content": comment.content,
                    "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            return Response({
                "status": False,
                "message": "Post not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
