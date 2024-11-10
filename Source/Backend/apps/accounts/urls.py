from django.urls import path
from . import views

urlpatterns = [
    path('register', views.mock_register, name='mock_register'),
    path('login', views.mock_login, name='mock_login'),
    path('',views.home),
    path('logout',views.logout_view),
    path('googleLogin/', views.homere, name='homere'),
    path('redirect', views.red, name='red')
   
]
