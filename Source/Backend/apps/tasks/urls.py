from django.urls import path 
from . import views 

urlpatterns = [
path('getTasksByGroupId', views.get_tasks_by_group, name='get_tasks_by_group'), 
path('addTask', views.add_task, name='add_task'), 
path('join', views.join_task, name='join_task'), 
path('leave', views.leave_task, name='leave_task'), 
path('finish', views.finish_task, name='finish_task'), 
path('review', views.review_task, name='review_task'), 
]