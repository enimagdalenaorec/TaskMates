from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from core.models import Task, UserTask
from django.utils import timezone

# 1. Get Basic User Info
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_basic_info(request):
    user = request.user
    response = {
        "profilePicture": None,  # Dodaj stvarnu logiku za sliku profila ako je implementirano
        "username": user.username,
        "email": user.email
    }
    return Response(response, status=HTTP_200_OK)

# 2. Get Active Tasks
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_tasks(request):
    user = request.user
    active_tasks = UserTask.objects.filter(user=user, task__status='not_finished')
    tasks = [
        {
            "id": task.task.id,
            "taskName": task.task.name,
            "groupName": task.task.group.name,
            "timeLeft": task.task.deadline - timezone.now(),
            "icon": task.task.icon,
            "points": task.task.points,
        }
        for task in active_tasks
    ]
    return Response({"tasks": tasks}, status=HTTP_200_OK)

# 3. Change Username
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_username(request):
    user = request.user
    data = request.data
    new_username = data.get("username")
    if not new_username:
        return Response({"error": "Username is required"}, status=HTTP_400_BAD_REQUEST)
    user.username = new_username
    user.save()
    return Response({"message": "Username updated successfully"}, status=HTTP_200_OK)

# 4. Change Profile Picture
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_profile_picture(request):
    user = request.user
    data = request.data
    profile_picture = data.get("profilePicture")
    if not profile_picture:
        return Response({"error": "Profile picture is required"}, status=HTTP_400_BAD_REQUEST)

    # Pretpostavka: Obrada slike u base64 ili slično; dodaj potrebnu logiku
    user.profilePicture = profile_picture
    user.save()
    return Response({"message": "Profile picture updated successfully"}, status=HTTP_200_OK)
