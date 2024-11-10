from django.urls import path 
from . import views 
path('get-all-groups', views.mock_admin_get_all_groups, name='mock_admin_get_all_groups'), 
path('find', views.mock_admin_find_group, name='mock_admin_find_group'), 
path('delete-group', views.mock_admin_delete_group, name='mock_admin_delete_group'), 
