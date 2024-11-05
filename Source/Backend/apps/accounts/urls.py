from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.mock_register, name='mock_register'),
    path('api/login/', views.mock_login, name='mock_login'),
]
