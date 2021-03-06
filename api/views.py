import re
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import generic
from rest_framework import generics, serializers, status, viewsets, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer
from rest_framework.authentication import BasicAuthentication
import requests
from django.contrib import auth
from rest_framework.authtoken.models import Token

# Create your views here.
def homepage(request):
    return HttpResponse("Hello World")

class LoginView(ObtainAuthToken):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        if request.data == {}:
            return Response(
                {"message": "Send request Body"}, status=status.HTTP_204_NO_CONTENT
            )
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                "token": token.key
                }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User/password doesn't match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, format=None):
        if request.data == {}:
            return Response(
                {"message": "Send request Body"}, status=status.HTTP_204_NO_CONTENT
            )

        register_serializer = RegistrationSerializer(data=request.data)
        if register_serializer.is_valid():
            register_serializer.save()
            return Response(
                {
                    "data": register_serializer.data,
                    "message": "You are succesfully registered",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def LogoutView(request):
    request.user.auth_token.delete()
    return Response({
            'message': "You are successfully logged out"
        }, status=status.HTTP_200_OK)
                

class ProfileView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        username = str(request.user)
        user = User.objects.get(username=username)
        if user is not None:
            return Response({
                "username": user.username,
                "email": user.email,
                "message": "You won't get results if your token is expired"
            })
        return Response({
            'message': "Your account is disabled. Please log in again"
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def version1(request):
    return Response({
        'version': request.version
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def version2(request):
    return Response({
        'version': request.version
    }, status=status.HTTP_200_OK)