from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .forms import CustomeUserRegistrationForm,UserLoginForm
from Posts.models import profile


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Now it uses Django's login()
            return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

 

def logout_view(request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('/users/login')
        else:
            return redirect('/users/login')
        

def register(request):
    if request.method == 'POST':
        form = CustomeUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            current_user=User.objects.get(username=form.cleaned_data['username'])
            profile.objects.create(
                user=current_user,
                profile_picture='profile_pictures/logo1.jpg'  # or 'profile_pictures/logo1.jpg' if in subfolder
            )
            return redirect('/users/login')  # redirect to login after successful signup
    else:
        form = CustomeUserRegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


def suggestedAccount(request):
    if request.user.is_authenticated:
        current_user = request.user
        following_users = current_user.following.all().values_list('user', flat=True)
        users = User.objects.exclude(id__in=following_users).exclude(id=current_user.id)
        
        profiles = profile.objects.filter(user__in=users)
        suggested_users = {
            'profiles': profiles
        }
        return render(request, 'users/suggested_accounts.html', {'suggested': suggested_users})
    else:
        return redirect('/users/login')
