from django.urls import path 
from . import views 

urlpatterns = [
path('/get-all-tasks', views.get_all_tasks, name='get_all_tasks'), 
]