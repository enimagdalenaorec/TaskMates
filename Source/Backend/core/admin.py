from django.contrib import admin
from .models import User, Notification, Group, GroupUser, Task, UserTask, Rating
# Register your models here.
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Group)
admin.site.register(GroupUser)
admin.site.register(Task)
admin.site.register(UserTask)
admin.site.register(Rating)