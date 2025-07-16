from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .forms import CustomeUserRegistrationForm,UserLoginForm


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
            return redirect('/users/login')  # redirect to login after successful signup
    else:
        form = CustomeUserRegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


 