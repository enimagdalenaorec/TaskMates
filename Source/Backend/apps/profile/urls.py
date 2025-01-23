from django.urls import path 
from . import views

urlpatterns = [
    path('get-basic-info', views.get_basic_info, name='get_basic_info'),
    path('get-active-tasks', views.get_active_tasks, name='get_active_tasks'),
    path('change-username', views.change_username, name='change_username'),
    path('change-profile-picture', views.change_profile_picture, name='change_profile_picture'),
]
