
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate ,login as auth_login, logout as auth_logout
from users.models import User
from customer.models import *
from organizer.models import*
from api.v1.organizer.serializer import EventSerializer




@api_view(['POST'])
@permission_classes([AllowAny])
def register_organizer(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    phone = request.data.get('phone')

    if User.objects.filter(email=email).exists():
        response_data={
            "status_code": 6001,
            "data": {},
            "message": "User already exists"
        }
        return Response(response_data)

   
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )
    user.save()

    organizer = Organizer.objects.create(user=user)
    organizer.save()

 
    refresh = RefreshToken.for_user(user)

    return Response({
        "status_code": 6000,
        "data": {
            "access": str(refresh.access_token),
        },
        "message": "Organizer registration successful"
    })

@api_view(['GET'])
@permission_classes([AllowAny])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_events(request):
   
    organizer = Organizer.objects.get(user=request.user)
    events = Event.objects.filter(organizer=organizer).order_by('-start_at')
    serializer = EventSerializer(events, many=True, context={"request": request})

    response_data = {
        "status_code": 6000,
        "data": serializer.data,
        "message": "My events retrieved successfully"
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def event_detail_organizer(request, id):
  
    organizer = Organizer.objects.filter(user=request.user).first()
    if not organizer:
        return Response({"error": "Organizer profile not found."})

   
    event = Event.objects.filter(id=id, organizer=organizer).first()
    if not event:
        return Response({"error": "Event not found or you don't have access."})

   
    serializer = EventSerializer(event, context={"request": request})
    return Response({
        "status_code": 6000,
        "data": serializer.data,
        "message": "Event details retrieved successfully"
    })


@api_view(['POST'])
@permission_classes([AllowAny])  
def create_event(request):
    data = request.data
    serializer = EventSerializer(data=data)

    if serializer.is_valid():
        organizer = None
        if request.user.is_authenticated:
            
            
         organizer = Organizer.objects.get(user=request.user)
            
              

        event = serializer.save(organizer=organizer)
        context = {"request": request}

        response_data = {
            "status_code": 6000,
            "data": EventSerializer(event, context=context).data,
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



@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_event(request,id):
    event=Event.objects.get(id=id)
    event.delete()

    response_data={
        "status_code":6000,
        "message": "Event deleted successfully."

    }


    return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
   
    response_data={
        "status_code": 6000,
        "message": "Logout successful. Please remove tokens from client."
    }


    return Response(response_data)

    


