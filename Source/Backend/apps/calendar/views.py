from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from core.models import Task

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Korisnik mora biti autentificiran
def get_all_tasks(request):
    tasks = Task.objects.all()
    response_data = [
        {
            "id": task.id,
            "name": task.name,
            "icon": task.icon,
            "deadline":task.deadline  
                # Ovo može biti None ako ikona nije definirana
        }
        for task in tasks
    ]

    return Response({"tasks": response_data}, status=HTTP_200_OK)
