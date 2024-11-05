from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Mock endpoint za dohvat grupa
@api_view(['GET'])
def mock_get_groups(request):
    return Response({
        "groups": [
            {"name": "Group1", "image": "base64image1", "id": "1"},
            {"name": "Group2", "image": "base64image2", "id": "2"},
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
            {"name": "Member1", "picture": "base64picture1"},
            {"name": "Member2", "picture": "base64picture2"},
        ]
    }, status=HTTP_200_OK)

# Mock endpoint za dohvat koda i linka grupe
@api_view(['POST'])
def mock_get_group_code_link(request):
    return Response({
        "code": "sample_code",
        "link": "https://example.com/join/sample_code"
    }, status=HTTP_200_OK)