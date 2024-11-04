from django.urls import path 
from . import views 
path('api/groups', views.mock_get_groups, name='mock_get_groups'), 
path('api/groups/join', views.mock_join_group, name='mock_join_group'), 
path('api/groups/create', views.mock_create_group, name='mock_create_group'), 
