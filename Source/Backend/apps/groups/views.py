from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from core.models import Group
from core.models import GroupUser


@api_view(['GET'])
def get_groups(request):
    # Dohvati sve grupe u kojima je autentificirani korisnik član
    groups = Group.objects.filter(groupuser__user=request.user)

    groups_data = [
        {
            "id": group.id,
            "name": group.name,
            # "image": group.image.url if group.image else None,
            "expiringSoonCount": 0,
            "unreadMessagesCount": 0
        }
        for group in groups
    ]

    return Response({"groups": groups_data}, status=status.HTTP_200_OK)

# Mock endpoint za pridruživanje grupi
@api_view(['POST'])
def join_group(request):
    code = request.data.get('code', None)

    if not code:
        return Response({"message": "Please provide a code."}, status=status.HTTP_400_BAD_REQUEST)

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
    

# Mock endpoint za kreiranje grupe
@api_view(['POST'])
def create_group(request):
    name=request.data.get("name")
    if not name:
        return Response({
            "error": "Group name is required."
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        group=Group.objects.create(name=name)
        return Response({
            "id": group.id,
            "message": "Group created successfully."
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_all_members(request):
    group_id = request.data.get("group_id", None)

    if not group_id:
        return Response({"message": "group_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    # Dohvaćamo sve članove grupe preko GroupUser tablice
    group_users = GroupUser.objects.filter(group=group)

    # Serijalizacija članova
    members_data = [
        {
            "name": gu.user.username,
            "picture": None,  # Ako nemate profilePicture, postavite ga kasnije ili ostavite None
            "userId": gu.user.id
        }
        for gu in group_users
    ]

    return Response({"members": members_data}, status=status.HTTP_200_OK)

# Mock endpoint za dohvat koda
@api_view(['POST'])
def get_group_code(request):
    group_id = request.data.get("group_id", None)

    if not group_id:
        return Response({"message": "group_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    # Vraćamo join_code grupe
    return Response({"code": str(group.join_code)}, status=status.HTTP_200_OK)