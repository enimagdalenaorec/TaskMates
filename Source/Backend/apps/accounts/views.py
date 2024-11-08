from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout

# Mock endpoint za registraciju
@api_view(['POST'])
def mock_register(request):
    return Response({
        "refresh": "sample_refresh_token",
        "access": "sample_access_token",
        "user": {
            "id": 1,
            "username": "newuser",
            "email": "newuser@example.com",
            "nickname": "NewUser",
        }
    }, status=status.HTTP_200_OK)

# Mock endpoint za prijavu
@api_view(['POST'])
def mock_login(request):
    return Response({
        "refresh": "sample_refresh_token",
        "access": "sample_access_token",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "testuser@example.com",
            "nickname": "Tester",
            "profile_image": "https://example.com/path/to/profile_image.jpg",
            "points": 150
        }
    }, status=status.HTTP_200_OK)

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

@api_view(['GET'])
def google_login(request):
    return redirect("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id=564641218259-mnod8begp6q5b2tilo68qkegdcg73iiu.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccounts%2Fgoogle%2Flogin%2Fcallback%2F&scope=profile%20email&response_type=code&state=erMbwcLOXBTvTGk9&access_type=online&service=lso&o2v=2&ddm=1&flowName=GeneralOAuthFlow")