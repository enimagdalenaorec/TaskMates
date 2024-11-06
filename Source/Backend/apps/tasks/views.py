from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Mock endpoint za dohvat zadataka po grupi
@api_view(['POST'])
def mock_get_tasks_by_group(request):
    return Response({
        "tasks": [
            {"id": "1", "name": "Task1", "icon": None, "deadline": "2023-12-31", "members": [{"name": "Member1"}],"groupId":1},
            {"id": "2", "name": "Task2", "icon": None, "deadline": "2023-12-31", "members": [{"name": "Member2"}],"groupId":1}
        ]
    }, status=HTTP_200_OK)

# Mock endpoint za dodavanje novog zadatka
@api_view(['POST'])
def mock_add_task(request):
    return Response({
        "message": "success"
    }, status=HTTP_200_OK)

# Mock endpoint za pridruživanje zadatku
@api_view(['POST'])
def mock_join_task(request):
    return Response({
        "message": "success"
    }, status=HTTP_200_OK)

# Mock endpoint za napuštanje zadatka
@api_view(['POST'])
def mock_leave_task(request):
    return Response({
        "message": "success"
    }, status=HTTP_200_OK)

# Mock endpoint za završavanje zadatka
@api_view(['POST'])
def mock_finish_task(request):
    return Response({
        "message": "success"
    }, status=HTTP_200_OK)

# Mock endpoint za ocjenjivanje zadatka
@api_view(['POST'])
def mock_review_task(request):
    return Response({
        "message": "success"
    }, status=HTTP_200_OK)
