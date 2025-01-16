from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.get_groups, name='get_groups'),
    path('join', views.join_group, name='join_group'),
    path('create', views.create_group, name='create_group'),
    path('getAllMembers', views.get_all_members, name='get_all_members'),
    path('getGroupCodeLink', views.get_group_code, name='get_group_code'),
    path('leave', views.leave_group, name='leave_group'),  # Dodan URL za leave_group

]