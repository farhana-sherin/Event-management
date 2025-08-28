
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
def login(request):
    email = request.data.get("email")
    password=request.data.get("password")


    user=authenticate(email=email, password=password)
    if user:
        refresh= RefreshToken.for_user(user)
        response_data={
            "status_code":6000,
            "data":{
                "accesss":str(refresh.access_token),

            },
            "message":"login successfull"

        }
    else:
        response_data={
            "status_code":6000,
            "message":"invalid credentials"
        }

    return Response(response_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    phone = request.data.get('phone')
    

    if User.objects.filter(email=email).exists():
        return Response({
            "status_code": 6001,
            "data": {},
            "message": "User already exists"
        })

    
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )
    user.save()


    customer = Customer.objects.create(user=user)
    customer.save()

   
    refresh = RefreshToken.for_user(user)

    return Response({
        "status_code": 6000,
        "data": {
            "access": str(refresh.access_token),
            
            "role": role,
        },
        "message": "Registration successful "
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def profile(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    



    response_data = {
        "status_code": 6000,
        "data": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "phone": user.phone
        },
        "message": "Profile retrieved successfully"
    }
    return Response(response_data)



@api_view(['PUT'])
@permission_classes([AllowAny])
def update_profile(request):
    user=request.user
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.username = request.data.get('username', user.username)
    user.email = request.data.get('email', user.email)
    user.phone = request.data.get('phone', user.phone)
    user.save()


    response_data = {
        "status_code": 6000,
        "data":{
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "phone": user.phone

        },
        "message": "Profile updated successfully"
    }
    return Response(response_data)



@api_view(['POST'])
@permission_classes([AllowAny])
def serach_eventby_category(request):
    category = request.data.get('category')
    events = Event.objects.filter(category__iexact=category)
    context = {"request": request}

    serializer = EventSerializer(events, many=True, context=context)

    response_data = {
        "status_code": 6000,
        "data": serializer.data,
        "message": f"Events in category '{category}'"
    }

    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def events_list(request):
    events=Event.objects.all().order_by('-start_at') 
    serializer = EventSerializer(events, many=True, context={'request': request})


    response_data={
        "status_code":6000,
        "data":
            serializer.data,
        "message":"Events retrieved successfully"
    }

    return Response(response_data)










    





    



