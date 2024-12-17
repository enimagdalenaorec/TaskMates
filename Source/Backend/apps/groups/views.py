from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Mock endpoint za dohvat grupa
@api_view(['GET'])
def mock_get_groups(request):
    return Response({
        "groups": [
            {"name": "Group1", "image": "base64image1", "id": "1", "expiringSoonCount": "1", "unreadMessagesCount": "4"},
            {"name": "Group2", "image": "base64image2", "id": "2", "expiringSoonCount": "0", "unreadMessagesCount": "0"},
            {"name": "Group3", "image": "base64image3", "id": "3", "expiringSoonCount": "0", "unreadMessagesCount": "2"},
        ]
    }, status=HTTP_200_OK)

# Mock endpoint za pridruživanje grupi
@api_view(['POST'])
def mock_join_group(request):
    return Response({
        "message": "success"
    }, status=HTTP_200_OK)

# Mock endpoint za kreiranje grupe
@api_view(['POST'])
def create_group(request):
    # Izvuci parametar 'name' iz request.data
    group_name = request.data.get('name')

    # Validacija: Provjeri je li naziv grupe poslan
    if not group_name:
        return Response({
            "error": "Group name is required."
        }, status=HTTP_400_BAD_REQUEST)

    try:
        # Kreiraj novu grupu
        group = Group.objects.create(name=group_name)

        # Vrati uspješan odgovor s podacima o grupi
        return Response({
            "message": "Group created successfully.",
            "group": {
                "id": group.id,
                "name": group.name,
                "join_code": group.join_code,
                "created_at": group.created_at
            }
        }, status=HTTP_201_CREATED)

    except Exception as e:
        # Vrati grešku ako nešto pođe po zlu
        return Response({
            "error": str(e)
        }, status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mock_get_all_members(request):
    return Response({
        "members": [
            {"name": "Member1", "picture": "base64picture1", "userId":1},
            {"name": "Member2", "picture": "base64picture2", "userId":2},
        ]
    }, status=HTTP_200_OK)

# Mock endpoint za dohvat koda i linka grupe
@api_view(['POST'])
def mock_get_group_code_link(request):
    return Response({
        "code": "sample_code",
        "link": "https://example.com/join/sample_code"
    }, status=HTTP_200_OK)