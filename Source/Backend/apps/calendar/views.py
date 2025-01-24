from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from core.models import Task, UserTask

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_tasks(request):
    user = request.user
    
    # Dohvatimo sve UserTask zapise koji nisu finished ili failed
    user_tasks = UserTask.objects.filter(user=user).exclude(task__status__in=['finished', 'failed'])
    
    # Iz svakog UserTask objekta dohvatimo pripadajući Task i formiramo response
    response_data = [
        {
            "id": user_task.task.id,
            "name": user_task.task.name,
            "icon": user_task.task.icon,
            "deadline": user_task.task.deadline
        }
        for user_task in user_tasks
    ]
    
    return Response({"tasks": response_data}, status=HTTP_200_OK)
