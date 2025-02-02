"""
URL configuration for TaskMatesBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/profile/', include('apps.profile.urls')), 
    path('api/accounts/', include('apps.accounts.urls')), 
    path('api/calendar/', include('apps.calendar.urls')), 
    path('api/groups/', include('apps.groups.urls')), 
    path('api/notifications/', include('apps.notifications.urls')), 
    path('api/tasks/', include('apps.tasks.urls')), 
    path('accounts/',include("allauth.urls")), 
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('management/', include('apps.management.urls')),
]
