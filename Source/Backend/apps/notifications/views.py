from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.shortcuts import render

# Mock endpoint za dohvat svih notifikacija
@api_view(['GET'])
def get_notifications(request):
    user = request.user
    notifications = user.notifications.all()  # Pretpostavimo da imaš model za notifikacije
    data = [{'message': n.message, 'is_read': n.is_read} for n in notifications]
    return Response({'notifications': data}, status=200)