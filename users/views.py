from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .forms import CustomeUserRegistrationForm, AuthenticationForm


# Create your views here.
def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'users/login.html')

 

def logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('/login')
        else:
            return redirect('/login')

def register(request):
    print("Register view called")
    if request.method == 'POST':
        form = CustomeUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/login')  # redirect to login after successful signup
    else:
        print("Not a POST request")
        form = CustomeUserRegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


class login(APIView):

    def post(self,request):

        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return HttpResponse("You are not logged in. Please log in to access this page.")