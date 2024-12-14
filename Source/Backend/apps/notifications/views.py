from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Mock endpoint za dohvat svih notifikacija
@api_view(['GET'])
def mock_get_notifications(request):
    return Response({
        "notifications": [
            {"message": "You have 6 hours to finish task XY in group XY",
             "sentAt": "2024-05-12"},
            {"message": "Ana was added to group XY",
             "sentAt": "2024-06-12"},
        ]
    }, status=HTTP_200_OK)
