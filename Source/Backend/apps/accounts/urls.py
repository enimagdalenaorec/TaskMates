from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('logout',views.logout_view),
    path('googleLogin/', views.homere, name='homere'),
    path('redirect', views.red, name='red'),

   
]
