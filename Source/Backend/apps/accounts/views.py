from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

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
