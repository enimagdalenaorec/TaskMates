from django.urls import path 
from . import views 

urlpatterns = [
path('', views.mock_get_groups, name='mock_get_groups'), 
path('join', views.mock_join_group, name='mock_join_group'), 
path('create', views.mock_create_group, name='mock_create_group'), 
path('getAllMembers', views.mock_get_all_members, name='mock_get_all_members'), 
path('getGroupCodeLink', views.mock_get_group_code_link, name='mock_get_group_code_link'), 
]