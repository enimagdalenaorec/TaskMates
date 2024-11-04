from django.urls import path 
from . import views 
path('api/users/register', views.mock_register, name='mock_register'), 
path('api/users/login', views.mock_login, name='mock_login'), 
