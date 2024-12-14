from django.urls import path 
from . import views 

urlpatterns = [
path('get-all', views.mock_get_notifications, name='mock_get_notifications'), 
]