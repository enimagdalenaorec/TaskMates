from django.core.management.base import BaseCommand
from django.utils.timezone import now
from core.models import Task, UserTask, GroupUser, Notification
from hashlib import md5
from myproject.utils.emailsender import send_email

class Command(BaseCommand):
    help = "Check deadlines for tasks and send notifications accordingly."

    def handle(self, *args, **kwargs):
        tasks = Task.objects.filter(status__in=['available', 'full'])
        for task in tasks:
            self.check_task_deadline(task)
        self.stdout.write("Deadline check completed.")

    def check_task_deadline(self, task):
        remaining_time = (task.deadline - now()).total_seconds()
        total_time = (task.deadline-task.created_at).total_seconds()
        if remaining_time > 0 and remaining_time<=0.2*total_time:
            # Notify about approaching deadline
            self.send_approaching_deadline_notifications(task)
        elif remaining_time <= 0:
            # Notify about expired task
            self.send_expired_task_notifications(task)

    def send_approaching_deadline_notifications(self, task):
        user_task_count = UserTask.objects.filter(task=task).count()

        if user_task_count == 0:
            group_users = GroupUser.objects.filter(group=task.group)
            for group_user in group_users:
                unique_id = self.generate_unique_id(task, group_user.user, "approaching")
                if not Notification.objects.filter(unique_identifier=unique_id).exists():
                    Notification.objects.create(
                        message=f"No one has claimed the task '{task.name}', and its deadline is approaching!",
                        reciever=group_user.user,
                        unique_identifier=unique_id
                    )
                    send_email(group_user.user.email,'Task unclaimed',f"No one has claimed the task '{task.name}', and its deadline is approaching!")
        else:
            user_tasks = UserTask.objects.filter(task=task)
            for user_task in user_tasks:
                unique_id = self.generate_unique_id(task, user_task.user, "approaching")
                if not Notification.objects.filter(unique_identifier=unique_id).exists():
                    Notification.objects.create(
                        message=f"The deadline for your task '{task.name}' is approaching!",
                        reciever=user_task.user,
                        unique_identifier=unique_id
                    )
                    send_email(user_task.user.email,'Deadline approaching',f"The deadline for your task '{task.name}' is approaching!")

    def send_expired_task_notifications(self, task):
     if task.status not in ['expired']:
        # Only send shame notification if the task has expired
        user_task_count = UserTask.objects.filter(task=task).count()
        
        # Check if the task has users assigned to it
        if user_task_count > 0:
            group_users = GroupUser.objects.filter(group=task.group)
            for group_user in group_users:
                unique_id = self.generate_unique_id(task, group_user.user, "expired")
                if not Notification.objects.filter(unique_identifier=unique_id).exists():
                    Notification.objects.create(
                        message=f"The task '{task.name}' has expired, and it was not completed. Shame on the team!",
                        reciever=group_user.user,
                        unique_identifier=unique_id
                    )
                    send_email(group_user.user.email,'Task failed',f"The task '{task.name}' has expired, and it was not completed. Shame on the team!")

            # Optionally update the task's status to avoid further notifications
        task.status = 'expired'
        task.save()

    def generate_unique_id(self, task, user, notification_type):
        """
        Generate a unique identifier for a notification.
        """
        unique_string = f"{task.id}-{user.id}-{notification_type}"
        return md5(unique_string.encode('utf-8')).hexdigest()