from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Mock endpoint za dohvat svih grupa za admina
@api_view(['GET'])
def mock_admin_get_all_groups(request):
    return Response({
        "groups": [
            {"name": "Group1", "image": "base64image1", "id": "1"},
            {"name": "Group2", "image": "base64image2", "id": "2"},
        ]
    }, status=HTTP_200_OK)

# Mock endpoint za pretraživanje grupe po imenu
@api_view(['POST'])
def mock_admin_find_group(request):
    return Response({
        "name": request.data.get("groupName", "Group1"),
        "image": "base64image1"
    }, status=HTTP_200_OK)

# Mock endpoint za brisanje grupe
@api_view(['POST'])
def mock_admin_delete_group(request):
    return Response({
        "message": "success"
    }, status=HTTP_200_OK)
        