from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse(f"Welcome to the home page of the social {request.user.username} media app!")