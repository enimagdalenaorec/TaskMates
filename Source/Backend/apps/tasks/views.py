from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from django.utils import timezone

from core.models import Task, UserTask, Group, Rating, GroupUser

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Korisnik mora biti prijavljen
def get_task_by_id(request):
    from .serializers import GetTaskByIdSerializer

    serializer = GetTaskByIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    task_id = serializer.validated_data['taskId']

    # 1. Dohvatiti task
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)

    task.update_status()

    # 2. Dohvatiti članove koji sudjeluju
    user_tasks = UserTask.objects.filter(task=task)
    members = [
        {
            "name": ut.user.username,
            "picture": None  # Dodajte logiku ako korisnik ima sliku
        }
        for ut in user_tasks
    ]

    current_capacity = user_tasks.count()

    # 3. Izračun preostalog vremena
    now = timezone.now()
    time_left = (task.deadline - now).total_seconds()
    if time_left < 0:
        time_left = 0  # Ako je rok prošao, postavite na 0

    # 4. Provjeriti je li korisnik već ocijenio zadatak
    already_reviewed = Rating.objects.filter(task=task, sender=request.user).exists()

    # 5. Vratiti odgovor
    response_data = {
        "groupName": task.group.name,
        "taskName": task.name,
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
    from .serializers import GetTasksByGroupSerializer

    serializer = GetTasksByGroupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    group_id = serializer.validated_data['groupId']

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=HTTP_404_NOT_FOUND)

    tasks = Task.objects.filter(group=group)
    response_data = []
    for task in tasks:
        # Update the task's status before including it in the response
        task.update_status()

        user_tasks = UserTask.objects.filter(task=task)
        members = [{"name": ut.user.username} for ut in user_tasks]
        current_capacity = user_tasks.count()

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
            "groupName": group.name,
            "currentCapacity": current_capacity,
            "ts_deadline": task.deadline
        })

    return Response({"tasks": response_data}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # ili [IsAuthenticated], ovisno o vašim pravilima
def add_task(request):
    from .serializers import AddTaskSerializer

    serializer = AddTaskSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # Dohvaćamo validirane podatke
    name = serializer.validated_data['name']
    deadline_str = serializer.validated_data['deadline']
    group_id = serializer.validated_data['groupId']
    icon = serializer.validated_data.get('icon')  # Može biti None
    max_capacity = serializer.validated_data.get('max_capacity', 1)
    description = serializer.validated_data.get('description', '')
    points = serializer.validated_data.get('points', 100)

    # Provjeravamo postoji li group
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=HTTP_404_NOT_FOUND)

    # Parsiramo deadline
    try:
        deadline_dt = timezone.datetime.fromisoformat(deadline_str)
    except ValueError:
        return Response({"error": "Invalid deadline format."}, status=HTTP_400_BAD_REQUEST)

    # Kreiramo Task
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
    from .serializers import JoinTaskSerializer

    serializer = JoinTaskSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    task_id = serializer.validated_data["taskId"]

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)

    # Provjera da li je user u grupi
    if not GroupUser.objects.filter(user=request.user, group=task.group).exists():
        return Response({"error": "You are not a member of this group."}, status=HTTP_403_FORBIDDEN)

    # Check capacity
    current_count = UserTask.objects.filter(task=task).count()
    if current_count >= task.max_capacity:
        return Response({"error": "Task is at maximum capacity."}, status=HTTP_400_BAD_REQUEST)

    # Check if user is already in the task
    if UserTask.objects.filter(user=request.user, task=task).exists():
        return Response({"error": "You are already participating in this task."}, status=HTTP_400_BAD_REQUEST)

    UserTask.objects.create(user=request.user, task=task)
    task.update_status()
    return Response({"message": "success"}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_task(request):
    from .serializers import LeaveTaskSerializer

    serializer = LeaveTaskSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    task_id = serializer.validated_data['taskId']

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)

    try:
        user_task = UserTask.objects.get(user=request.user, task=task)
    except UserTask.DoesNotExist:
        return Response({"error": "You are not participating in this task."}, status=HTTP_400_BAD_REQUEST)

    user_task.delete()
    task.update_status()
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
        return Response({"error": "taskId and value are required."}, 
                        status=HTTP_400_BAD_REQUEST)

    # Dohvatimo Task
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=HTTP_404_NOT_FOUND)

    # 1) Provjera: Ako je korisnik SUDJELOVAO u zadatku, zabrani ocjenu.
    if UserTask.objects.filter(user=request.user, task=task).exists():
        return Response({"error": "Cannot review because you participated in this task."},
                        status=HTTP_403_FORBIDDEN)

    # 2) Provjera: Ako je korisnik već ostavio ocjenu za ovaj task, zabrani ponovno ocjenjivanje.
    if Rating.objects.filter(sender=request.user, task=task).exists():
        return Response({"error": "You have already left a review for this task."},
                        status=HTTP_403_FORBIDDEN)

    # 3) Pretvorimo dobiveni value u integer
    try:
        value_int = int(value)
    except ValueError:
        return Response({"error": "Value must be an integer."}, status=HTTP_400_BAD_REQUEST)

    # 4) Validacija da je rating u rasponu 1 - 5
    if not (1 <= value_int <= 5):
        return Response({"error": "Rating value must be between 1 and 5."}, 
                        status=HTTP_400_BAD_REQUEST)

    # 5) Kreiramo novi zapis u Rating jer su svi uvjeti zadovoljeni
    Rating.objects.create(sender=request.user, task=task, value=value_int)
    return Response({"message": "success"}, status=HTTP_200_OK)