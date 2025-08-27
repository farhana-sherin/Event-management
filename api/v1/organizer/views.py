
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate ,login as auth_login, logout as auth_logout
from users.models import User
from customer.models import *
from organizer.models import*
from api.v1.organizer.serializer import EventSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def list_event(request):
    events = Event.objects.all()
    context={
        "request": request
    }
    serializer = EventSerializer(events, many=True, context=context)

    return Response({
        "status_code": 6000,
        "data": serializer.data,
        "message": "Event fetch successful"
    })
