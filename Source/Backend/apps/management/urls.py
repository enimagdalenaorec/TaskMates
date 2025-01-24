# management/urls.py
from django.urls import path
from .views import run_check_deadlines
from . import views


urlpatterns = [
    path('run_check_deadlines/', run_check_deadlines, name='run_check_deadlines'),
    path('test_csrf/', views.test_csrf, name='test_csrf')
]