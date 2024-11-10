from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Mock endpoint za dohvat svih zadataka korisnika za kalendar
@api_view(['GET'])
def mock_get_all_tasks(request):
    return Response({
        "tasks": [
            {"icon": None, "name": "Task1", "id": "1"},
            {"icon": None, "name": "Task2", "id": "2"},
        ]
    }, status=HTTP_200_OK)
