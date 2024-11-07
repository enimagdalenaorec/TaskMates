from django.urls import path 
from . import views 

urlpatterns = [
path('getTasksByGroupId', views.mock_get_tasks_by_group, name='mock_get_tasks_by_group'), 
path('addTask', views.mock_add_task, name='mock_add_task'), 
path('join', views.mock_join_task, name='mock_join_task'), 
path('leave', views.mock_leave_task, name='mock_leave_task'), 
path('finish', views.mock_finish_task, name='mock_finish_task'), 
path('review', views.mock_review_task, name='mock_review_task'), 
]