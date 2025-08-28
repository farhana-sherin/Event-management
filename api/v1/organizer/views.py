
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

    response_data={
        "status_code": 6000,
        "data": serializer.data,
        "message": "Event fetch successful"
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([AllowAny])  
def create_event(request):
    data = request.data
    serializer = EventSerializer(data=data)

    if serializer.is_valid():
        
        organizer = request.user if request.user.is_authenticated else None
        event = serializer.save(organizer=organizer)
        context={
            "request":request
        }

        response_data = {
            "status_code": 6000,
            "data": EventSerializer(event,context=context).data,
            "message": "Event created successfully"
        }
        return Response(response_data)

    else:
        response_data = {
            "status_code": 6001,
            "errors": serializer.errors,
            "message": "Event creation failed"
        }
        return Response(response_data)



@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_event(request, id):
    
    event = Event.objects.get(id=id)
    

    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        response_data ={
            "status_code": 6000,
            "data": serializer.data,
            "message": "Event partially updated successfully"
        }
        return Response(response_data)

    


