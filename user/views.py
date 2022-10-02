from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
# Takes care of all the basic login, authenticizing and login process for tokenization
from django.contrib.auth import login, logout, authenticate
# The in-built django user module will take care of all the user related database functionality

#register a user
class RegisterView(APIView):

    def post(self, request, format='json'):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#login using username and password
@api_view(['GET', 'POST'])
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        authenticated = authenticate(username=username, password=password)
        print(username)
        if authenticated is not None and authenticated.is_active:
            login(request, authenticated)
            return Response("logged in successfully", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("login failed.Plese Check the username and password", status=status.HTTP_201_CREATED)


#Logouts the currently signed in user'
@api_view(['GET', 'POST'])
@csrf_exempt
def logout_user(request):
    logout(request)
    return Response("logged out successfully", status=status.HTTP_204_NO_CONTENT)

