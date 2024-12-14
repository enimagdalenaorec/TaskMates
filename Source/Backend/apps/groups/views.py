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
def mock_create_group(request):
    return Response({
        "message": "success"
    }, status=HTTP_200_OK)

@api_view(['POST'])
def mock_get_all_members(request):
    return Response({
        "members": [
            {"name": "Ana Anic", "picture": "base64picture1", "userId":1},
            {"name": "Eni Enić", "picture": "base64picture2", "userId":2},
            {"name": "Erna Ernić", "picture": "base64picture3", "userId":3},
            {"name": "Pero Perić", "picture": "base64picture4", "userId":4}
        ]
    }, status=HTTP_200_OK)

# Mock endpoint za dohvat koda i linka grupe
@api_view(['POST'])
def mock_get_group_code_link(request):
    return Response({
        "code": "ABC123",
        "link": "https://example.com/join/ABC123"
    }, status=HTTP_200_OK)