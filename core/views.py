from django.shortcuts import render,redirect
from Posts.models import profile

# Create your views here.


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