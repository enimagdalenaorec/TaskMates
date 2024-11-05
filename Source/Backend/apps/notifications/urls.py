from django.urls import path 
from . import views 

urlpatterns = [
path('api/notifications/get-all', views.mock_get_notifications, name='mock_get_notifications'), 
]