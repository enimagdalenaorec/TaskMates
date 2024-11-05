from django.urls import path 
from . import views 

urlpatterns = [
path('api/user/get-all-tasks', views.mock_get_all_tasks, name='mock_get_all_tasks'), 
]