from django.urls import path 
from . import views 

urlpatterns = [
path('api/tasks/get-tasks-by-group-id', views.mock_get_tasks_by_group, name='mock_get_tasks_by_group'), 
path('api/tasks/add-task', views.mock_add_task, name='mock_add_task'), 
path('api/tasks/join', views.mock_join_task, name='mock_join_task'), 
path('api/tasks/leave', views.mock_leave_task, name='mock_leave_task'), 
path('api/tasks/finish', views.mock_finish_task, name='mock_finish_task'), 
path('api/tasks/review', views.mock_review_task, name='mock_review_task'), 
]