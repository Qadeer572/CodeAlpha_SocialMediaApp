from django.shortcuts import render,redirect
from Posts.models import profile,Post,Followers
from django.contrib.auth.models import User

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        myProfile = profile.objects.get(user=request.user)
        totalLikes = 0
        totalPosts = 0

        post = Post.objects.filter(user=request.user)
        for p in post:
            totalPosts += 1
            totalLikes += p.likes.count()
        totalFollower= Followers.objects.filter(user=request.user).count()    
        context = {
            "profile": myProfile,
            "firstName": request.user.first_name,
            "lastName": request.user.last_name,
            "totalPosts": totalPosts,
            "totalLikes": totalLikes,
            "totalUsers": User.objects.count(),
            "totalFollower": totalFollower
        }

        if request.user.is_staff:
            context["users"] = User.objects.all()

        return render(request, 'core/dashboard.html', {'data': context})



def editProfile(request):
    if request.user.is_authenticated:
        Profile=profile.objects.get(user=request.user)
        user=request.user
        if request.method == 'POST':
            user.first_name = request.POST.get('firstName')
            user.last_name = request.POST.get('lastName')
            Profile.bio = request.POST.get('bio')

            if 'profile_picture' in request.FILES:
                Profile.profile_picture = request.FILES['profile_picture']

            user.save()
            Profile.save()
        context={
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "profile":Profile 
            }
        return render(request, 'core/editProfile.html',{'data':context})