from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Mock endpoint za dohvat zadataka po grupi
@api_view(['POST'])
def mock_get_tasks_by_group(request):
    return Response({
        "tasks": [
        {"id": "1", "name": "Task1", "description": "description1", "points": "300", "maxCapacity": "3", "status": "available", "picture": "", "icon": None, "deadline": "2024-12-31", "members": [{"name": "Member1"}, {"name": "Member2"}], "groupId": 1, "groupName": "Group1"},
        {"id": "2", "name": "Task2", "description": "description2", "points": "400", "maxCapacity": "2", "status": "full", "picture": "", "icon": None, "deadline": "2024-12-31", "members": [{"name": "Member2"}, {"name": "Member3"}], "groupId": 1, "groupName": "Group1"},
        {"id": "3", "name": "Task3", "description": "description3", "points": "500", "maxCapacity": "4", "status": "finished", "picture": "", "icon": None, "deadline": "2023-11-30", "members": [{"name": "Member3"}, {"name": "Member2"}, {"name": "Member3"}], "groupId": 2, "groupName": "Group2"},
        {"id": "4", "name": "Task4", "description": "description4", "points": "600", "maxCapacity": "5", "status": "failed", "picture": "", "icon": None, "deadline": "2023-10-31", "members": [{"name": "Member4"}], "groupId": 2, "groupName": "Group2"}
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
