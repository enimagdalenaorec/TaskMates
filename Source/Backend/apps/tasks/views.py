from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from rest_framework.permissions import AllowAny


from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from core.models import Task, UserTask, Group, Rating, GroupUser


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Korisnik mora biti prijavljen
def get_task_by_id(request):
    # Iz body-ja dohvatiti taskId
    task_id = request.data.get('taskId')
    if not task_id:
        return Response({"error": "taskId is required"}, status=HTTP_400_BAD_REQUEST)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)

    # Dohvatiti članove koji sudjeluju u zadatku
    user_tasks = UserTask.objects.filter(task=task)
    members = [
        {
            "name": ut.user.username,
            "picture": None  # Dodajte logiku ako korisnik ima sliku
        }
        for ut in user_tasks
    ]

    # Broj trenutno prijavljenih članova
    current_capacity = user_tasks.count()

    # Izračun preostalog vremena
    now = timezone.now()
    time_left = (task.deadline - now).total_seconds()
    if time_left < 0:
        time_left = 0  # Ako je rok prošao, postavite na 0

    # Provjeriti je li korisnik već ocijenio zadatak
    already_reviewed = Rating.objects.filter(task=task, sender=request.user).exists()

    # Priprema odgovora
    response_data = {
        "groupName": task.group.name,
        "taskName":task.name,
        "members": members,
        "maxCapacity": task.max_capacity,
        "currentCapacity": current_capacity,
        "description": task.description,
        "points": task.points,
        "status": task.status,
        "timeLeft": time_left,  # Vrijeme u sekundama do roka
        "alreadyReviewed": already_reviewed
    }

    return Response(response_data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_tasks_by_group(request):
    group_id = int(request.data.get('groupId'))
    if not group_id:
        return Response({"error": "groupId is required"}, status=HTTP_400_BAD_REQUEST)
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=HTTP_404_NOT_FOUND)
    
    # Get tasks for this group
    tasks = Task.objects.filter(group=group)
    response_data = []
    for task in tasks:
        # Get members for this task
        user_tasks = UserTask.objects.filter(task=task)
        members = [{"name": ut.user.username} for ut in user_tasks]

        response_data.append({
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "points": task.points,
            "max_capacity": task.max_capacity,
            "status": task.status,
            "icon": task.icon,
            "deadline": task.deadline.isoformat(),
            "members": members,
            "groupId": group.id,
            "groupName": group.name,  # Dodavanje naziva grupe ovdje
            "currentCapacity": len(members),
            "ts_deadline": task.deadline
        })
    
    return Response({"tasks": response_data}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
#@permission_classes([IsAuthenticated])
def add_task(request):
    # Expected fields: name, deadline, icon (optional), max_capacity, description, points, groupId
    name = request.data.get('name')
    deadline = request.data.get('deadline')
    group_id = request.data.get('groupId')
    icon = request.data.get('icon')
    max_capacity = request.data.get('max_capacity', 1)
    description = request.data.get('description', '')
    points = request.data.get('points', 100)

    if not (name and deadline and group_id):
        return Response({"error": "name, deadline, and groupId are required."}, status=HTTP_400_BAD_REQUEST)
    
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=HTTP_404_NOT_FOUND)
    
    try:
        # Parse deadline if needed, assuming frontend sends ISO8601 formatted string
        # If necessary, handle parsing or validation of the deadline.
        deadline_dt = timezone.datetime.fromisoformat(deadline)
    except ValueError:
        return Response({"error": "Invalid deadline format."}, status=HTTP_400_BAD_REQUEST)
    
    try:
        task = Task.objects.create(
            name=name,
            deadline=deadline_dt,
            icon=icon,
            max_capacity=max_capacity,
            description=description,
            points=points,
            group=group
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

    return Response({"message": "success", "taskId": task.id}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_task(request):
    # Expected field: taskId
    task_id = request.data.get('taskId')
    if not task_id:
        return Response({"error": "taskId is required"}, status=HTTP_400_BAD_REQUEST)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)

    # Check if user is in the same group
    if not GroupUser.objects.filter(user=request.user, group=task.group).exists():
        return Response({"error": "You are not a member of this group."}, status=HTTP_403_FORBIDDEN)

    # Check capacity
    current_count = UserTask.objects.filter(task=task).count()
    if current_count >= task.max_capacity:
        return Response({"error": "Task is at maximum capacity."}, status=HTTP_400_BAD_REQUEST)

    # Check if user already joined
    if UserTask.objects.filter(user=request.user, task=task).exists():
        return Response({"error": "You are already participating in this task."}, status=HTTP_400_BAD_REQUEST)

    UserTask.objects.create(user=request.user, task=task)
    return Response({"message": "success"}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_task(request):
    # Expected field: taskId
    task_id = request.data.get('taskId')
    if not task_id:
        return Response({"error": "taskId is required"}, status=HTTP_400_BAD_REQUEST)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)

    # Check if user is in the task
    try:
        user_task = UserTask.objects.get(user=request.user, task=task)
    except UserTask.DoesNotExist:
        return Response({"error": "You are not participating in this task."}, status=HTTP_400_BAD_REQUEST)

    user_task.delete()
    return Response({"message": "success"}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_task(request):
    # Expected field: taskId
    task_id = request.data.get('taskId')
    if not task_id:
        return Response({"error": "taskId is required"}, status=HTTP_400_BAD_REQUEST)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)

    # Optionally: Check if user has permission to finish the task (e.g., only members or admin)
    if not UserTask.objects.filter(user=request.user, task=task).exists():
        return Response({"error": "You are not a participant in this task."}, status=HTTP_403_FORBIDDEN)

    task.status = 'finished'
    task.save()
    return Response({"message": "success"}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_task(request):
    # Expected fields: taskId, value (1-5)
    task_id = request.data.get('taskId')
    value = request.data.get('value')
    if not (task_id and value is not None):
        return Response({"error": "taskId and value are required."}, status=HTTP_400_BAD_REQUEST)

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)
    
    # Check if user participated in the task before allowing rating
    if not UserTask.objects.filter(user=request.user, task=task).exists():
        return Response({"error": "You did not participate in this task."}, status=HTTP_403_FORBIDDEN)

    try:
        value_int = int(value)
    except ValueError:
        return Response({"error": "Value must be an integer."}, status=HTTP_400_BAD_REQUEST)

    # Validate the rating value
    if value_int < 1 or value_int > 5:
        return Response({"error": "Rating value must be between 1 and 5."}, status=HTTP_400_BAD_REQUEST)

    Rating.objects.create(sender=request.user, task=task, value=value_int)
    return Response({"message": "success"}, status=HTTP_200_OK)
