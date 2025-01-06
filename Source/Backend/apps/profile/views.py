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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_username(request):
    from .serializers import ChangeUsernameSerializer  # Uvezite serializer

    serializer = ChangeUsernameSerializer(data=request.data)
    if not serializer.is_valid():
        # Ako serializer nije validan, vraćamo grešku 400
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # Serializer je validiran, uzimamo podatak
    new_username = serializer.validated_data["username"]

    user = request.user
    user.username = new_username
    user.save()
    return Response({"message": "Username updated successfully"}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_profile_picture(request):
    from .serializers import ChangeProfilePictureSerializer

    serializer = ChangeProfilePictureSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    profile_picture = serializer.validated_data["profilePicture"]
    user = request.user

    # Ovisno o načinu čuvanja slike, ovdje može biti logika za dekodiranje base64 -> file
    # ili izravno pohranjivanje u polje ako već imate rješenje za to
    user.profilePicture = profile_picture
    user.save()
    return Response({"message": "Profile picture updated successfully"}, status=HTTP_200_OK)
