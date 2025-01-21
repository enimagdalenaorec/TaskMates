from core.models import Task, UserTask
from django.utils import timezone
import importlib

def update_status(task):
        current_capacity = UserTask.objects.filter(task=task).count()
        if task.status == 'finished' or task.status == 'failed':
            return  # Ne mijenjamo status ako je završen ili neuspješan

        if current_capacity >= task.max_capacity:
            task.status = 'full'
        elif current_capacity < task.max_capacity:
            task.status = 'available'

        now = timezone.now()
        if task.deadline < now:
            checkdeadlines = importlib.import_module('apps.management.commands.checkdeadlines')
            # Access the Command class and then call send_expired_task_notifications
            command_class = checkdeadlines.Command
            send_expired_task_notifications = command_class().send_expired_task_notifications
            send_expired_task_notifications(task)

        task.save()