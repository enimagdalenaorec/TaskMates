from django.urls import path 
from . import views 
path('api/admin/get-all-groups', views.mock_admin_get_all_groups, name='mock_admin_get_all_groups'), 
path('api/admin/find', views.mock_admin_find_group, name='mock_admin_find_group'), 
path('api/admin/delete-group', views.mock_admin_delete_group, name='mock_admin_delete_group'), 
