from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from core.models import Group
from core.models import GroupUser
import cloudinary.uploader
import base64
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes


 
cloudinary.config(
    cloud_name=settings.CLOUDINARY['CLOUD_NAME'],
    api_key=settings.CLOUDINARY['API_KEY'],
    api_secret=settings.CLOUDINARY['API_SECRET']
)

@api_view(['GET'])
def get_groups(request):
    # Dohvati sve grupe u kojima je autentificirani korisnik član
    groups = Group.objects.filter(groupuser__user=request.user)

    groups_data = [
        {
            "id": group.id,
            "name": group.name,
            "image": group.image if group.image else None,
            "expiringSoonCount": 0,
            "unreadMessagesCount": 0
        }
        for group in groups
    ]

    return Response({"groups": groups_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def join_group(request):
    from .serializers import JoinGroupSerializer  # ili gdje god je serializer definiran

    serializer = JoinGroupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    code = serializer.validated_data['code']

    # Pokušaj pronaći grupu s datim kodom
    try:
        group = Group.objects.get(join_code=code)
    except Group.DoesNotExist:
        return Response({"message": "No group found with the provided code."}, status=status.HTTP_404_NOT_FOUND)

    # Pokušaj dodati korisnika u grupu
    group_user, created = group.groupuser_set.get_or_create(user=request.user)

    if created:
        # Korisnik je uspješno dodan u grupu
        return Response({"message": "success"}, status=status.HTTP_200_OK)
    else:
        # Korisnik je već član grupe
        return Response({"message": "You are already a member of this group."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_group(request):
    from .serializers import CreateGroupSerializer

    serializer = CreateGroupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    name = serializer.validated_data['name']
    if serializer.validated_data['image']:
        imagebase64=serializer.validated_data['image'] #'image' is 64bit image
        image_data = imagebase64[22:]
        image_data = base64.b64decode(image_data)
        image_content = ContentFile(image_data, name="group_image.png")
        upload_result = cloudinary.uploader.upload(image_content)
        image_url = upload_result['url']
    else:
        image_url=None
    try:

        # Create the group
        group = Group.objects.create(name=name, image=image_url)

        # Automatically add the user who created the group as a member
        GroupUser.objects.create(user=request.user, group=group)

        return Response({
            "id": group.id,
            "message": "Group created successfully, and user added as a member.",
            "image_url": image_url  # Return the image URL in the response
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_all_members(request):
    from .serializers import GetAllMembersSerializer

    serializer = GetAllMembersSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    group_id = serializer.validated_data['group_id']

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    group_users = GroupUser.objects.filter(group=group)

    members_data = [
        {
            "name": gu.user.username,
            "picture": gu.user.profile_picture,  # Ako kasnije imate polje za profilePicture, ovdje ga možete dodati
            "userId": gu.user.id
        }
        for gu in group_users
    ]

    return Response({"members": members_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_group_code(request):
    from .serializers import GetGroupCodeSerializer

    serializer = GetGroupCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    group_id = serializer.validated_data['group_id']

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response({"code": str(group.join_code)}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_group(request):
    from .serializers import LeaveGroupSerializer

    serializer = LeaveGroupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    group_id = serializer.validated_data['groupId']

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        group_user = GroupUser.objects.get(user=request.user, group=group)
    except GroupUser.DoesNotExist:
        return Response({"error": "You are not a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

    group_user.delete()  # Remove the user's membership from the group
    return Response({"message": "success"}, status=status.HTTP_200_OK)