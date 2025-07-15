from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import APIView
from rest_framework.response import Response


# Create your views here.
def loginView(request):
    if request.user.is_authenticated:
        return redirect('/home')
    return render(request, 'users/login.html')


def logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('/login')
        else:
            return redirect('/login')
class login(APIView):

    def post(self,request):

        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return HttpResponse("You are not logged in. Please log in to access this page.")