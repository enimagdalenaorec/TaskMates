# management/urls.py
from django.urls import path
from .views import run_check_deadlines

urlpatterns = [
    path('run_check_deadlines/', run_check_deadlines, name='run_check_deadlines'),
]