from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'Posts/home.html')

def profile(request):
    print("Profile view called")
    if request.user.is_authenticated:
        return render(request, 'core/profile.html', {'user': request.user})
    else:
        return HttpResponse("You are not logged in. Please log in to access this page.")