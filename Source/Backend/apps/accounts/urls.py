from django.urls import path
from . import views

urlpatterns = [
    path('register', views.mock_register, name='mock_register'),
    path('login', views.mock_login, name='mock_login'),
]
