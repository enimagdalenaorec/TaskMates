from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from core.models import Task, UserTask

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Korisnik mora biti autentificiran
def get_all_tasks(request):
    user = request.user
    active_tasks = UserTask.objects.filter(user=user).exclude(task__status__in=['finished', 'failed'])
    response_data = [
        {
            "id": task.id,
            "name": task.name,
            "icon": task.icon,
            "deadline":task.deadline  
                # Ovo može biti None ako ikona nije definirana
        }
        for task in active_tasks
    ]

    return Response({"tasks": response_data}, status=HTTP_200_OK)
