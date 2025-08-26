
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate ,login as auth_login, logout as auth_logout
from users.models import User
from customer.models import *
from organizer.models import*



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

    # Create user
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
        "message": f"Registration successful "
    })

    





    



