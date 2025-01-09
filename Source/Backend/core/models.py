from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone  # Import timezone for DateTimeField default
from django.conf import settings
from django.core.exceptions import ValidationError
import random

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # This hashes the password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    #profilePicture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) 
        #Treba postavit MEDIA_ROOT
    is_staff = models.BooleanField(default=False)  # Necessary for admin access

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    time_sent_at = models.DateTimeField(default=timezone.now)  # Automatically set to current time
    message = models.TextField()  # Field to store the notification message
    reciever = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # References your custom User model
        on_delete=models.CASCADE,  # Deletes notifications if the user is deleted
        related_name='notifications'  # Allows reverse lookup: user.notifications.all()
    )

    def __str__(self):
        return f"Notification for {self.reciever.username} - {'Read' if self.is_read else 'Unread'}"
    
class Group(models.Model):
    name = models.CharField(max_length=100)  # Group name
    #image = models.ImageField(upload_to='group_images/', blank=True, null=True)  # Optional image for the group
          #Treba setupat Media Root
    join_code = models.PositiveSmallIntegerField(unique=True)  # Unique short integer for joining

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): #Bitno da join_code bude postavljen i jedinstven
        if not self.join_code:  # Only generate a join_code if it's not set
            self.join_code = self.generate_join_code()
        super().save(*args, **kwargs)    

    def generate_join_code(self):
        #Generate a random unique join code.
        while True:
            code = random.randint(100000, 999999)  # Generate a random 6-digit number
            if not Group.objects.filter(join_code=code).exists():  # Ensure it's unique
                return code

    def join_group(self, user):
        #Function to allow a user to join the group.#
        if not isinstance(user, settings.AUTH_USER_MODEL):
            raise ValidationError("Invalid user.")
        
        group_user, created = GroupUser.objects.get_or_create(group=self, user=user)
        return group_user

class GroupUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to User
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # Reference to Group

    class Meta:
        unique_together = ('user', 'group')  # Ensure a user can only join a group once

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"
    

class Task(models.Model):
    name = models.CharField(max_length=100)
    #picture = models.ImageField(upload_to='task_pics/', blank=True, null=True)  # Field for task image
      #setup media root
    deadline = models.DateTimeField(default=timezone.now)  # Deadline for task completion
    STATUS_CHOICES = [
        ('full', 'Full'),
        ('available', 'Available'),
        ('finished', 'Finished'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    icon = models.CharField(max_length=50, blank=True, null=True)  # Icon representation of the task
    max_capacity = models.PositiveIntegerField(default=1)  # Maximum number of users for the task
    description = models.TextField(blank=True, null=True)  # Task description
    points = models.IntegerField(default=100)  # Points associated with the task (can be negative)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1) 
    
    def update_status(self):
        current_capacity = UserTask.objects.filter(task=self).count()
        if self.status == 'finished' or self.status == 'failed':
            return  # Ne mijenjamo status ako je završen ili neuspješan

        if current_capacity >= self.max_capacity:
            self.status = 'full'
        elif current_capacity < self.max_capacity:
            self.status = 'available'

        now = timezone.now()
        if self.deadline < now:
            self.status = 'failed'

        self.save()

    def save(self, *args, **kwargs):
        if self.max_capacity < 1 or self.max_capacity > 5:
            raise ValueError("Max capacity must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class UserTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Linking to the User model
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Linking to the Task model

    def __str__(self):
        return f"{self.user.username} - {self.task.name}"
    
class Rating(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User who sends the rating
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # The task being rated
    value = models.IntegerField(default=1)  # Rating value (should be between 1 and 5)

    def save(self, *args, **kwargs):
        if self.value < 1 or self.value > 5:
            raise ValueError("Rating value must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rating from {self.sender.username} for {self.task.name}: {self.value}"
    
