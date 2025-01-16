from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.shortcuts import render

@api_view(['GET'])
def get_notifications(request):
    """
    Dohvat svih notifikacija za trenutno prijavljenog korisnika.
    Vraća poruku, status 'is_read', i vrijeme slanja.
    """
    user = request.user
    notifications = user.notifications.all()  # Pretpostavka da User ima 'notifications' relaciju
    data = [
        {
            'message': n.message,
            'sent_at': format(n.time_sent_at, 'Y-m-d H:i:s'),  # Formatirano vrijeme
            'is_read': n.is_read
        }
        for n in notifications
    ]
    return Response({'notifications': data}, status=HTTP_200_OK)
