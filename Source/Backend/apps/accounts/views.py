from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout
import uuid
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def check_authentication(request):
    print('user je ',request.user)
    print('request ',request)
    if request.user.is_authenticated:
        return Response({'is_authenticated': True}, status=200)
    else:
        return Response({'is_authenticated': False}, status=200)

def home(request):
    return render(request, "home.html")

@api_view(['GET'])
@permission_classes([AllowAny])
def red(request):
    return redirect('/accounts/google/login/')


@api_view(['GET'])
@permission_classes([AllowAny])
def homere(request):
    return redirect("https://taskmatesbackend-pd5h.onrender.com/api/accounts/redirect") 
def logout_view(request):
    logout(request)
    return redirect("/")

# @api_view(['GET'])
# def google_login(request):
#     return redirect("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id=564641218259-mnod8begp6q5b2tilo68qkegdcg73iiu.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccounts%2Fgoogle%2Flogin%2Fcallback%2F&scope=email%20profile&response_type=code&state=G5RSd8mlbnU55zfw&access_type=online&service=lso&o2v=2&ddm=1&flowName=GeneralOAuthFlow")