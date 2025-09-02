from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from users.models import User
from customer.models import *
from organizer.models import *
from payments.models import *
from api.v1.organizer.serializer import *
from api.v1.customer.views import notify_event_update, create_notification


# ------------------- AUTH -------------------

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
    organizer = Organizer.objects.create(user=user)

    refresh = RefreshToken.for_user(user)

    return Response({
        "status_code": 6000,
        "data": {"access": str(refresh.access_token)},
        "message": "Organizer registration successful"
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({
        "status_code": 6000,
        "message": "Logout successful. Please remove tokens from client."
    })


# ------------------- EVENTS -------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_events(request):
    organizer = Organizer.objects.get(user=request.user)
    events = Event.objects.filter(organizer=organizer).order_by('-start_at')
    serializer = EventSerializer(events, many=True, context={"request": request})

    return Response({
        "status_code": 6000,
        "data": serializer.data,
        "message": "My events retrieved successfully"
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def event_detail_organizer(request, id):
    organizer = Organizer.objects.filter(user=request.user).first()
    if not organizer:
        return Response({"status_code": 6001, "message": "Organizer profile not found"})

    event = Event.objects.filter(id=id, organizer=organizer).first()
    if not event:
        return Response({"status_code": 6001, "message": "Event not found or access denied"})

    serializer = EventSerializer(event, context={"request": request})
    return Response({
        "status_code": 6000,
        "data": serializer.data,
        "message": "Event details retrieved successfully"
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    serializer = EventSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        organizer = Organizer.objects.get(user=request.user)
        event = serializer.save(organizer=organizer)

        return Response({
            "status_code": 6000,
            "data": EventSerializer(event, context={"request": request}).data,
            "message": "Event created successfully"
        })

    return Response({
        "status_code": 6001,
        "errors": serializer.errors,
        "message": "Event creation failed"
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_event(request, id):
    organizer = Organizer.objects.get(user=request.user)
    event = Event.objects.get(id=id, organizer=organizer)

    serializer = EventSerializer(event, data=request.data, partial=True, context={"request": request})
    if serializer.is_valid():
        updated_event = serializer.save()

        # 🔔 Notify all customers about update
        notify_event_update(updated_event)

        return Response({
            "status_code": 6000,
            "data": serializer.data,
            "message": "Event updated successfully"
        })

    return Response({
        "status_code": 6001,
        "errors": serializer.errors,
        "message": "Event update failed"
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, id):
    organizer = Organizer.objects.get(user=request.user)
    event = Event.objects.get(id=id, organizer=organizer)

    # 🔔 Notify all customers about deletion
    bookings = Booking.objects.filter(event=event)
    for booking in bookings:
        create_notification(
            customer=booking.customer,
            title="Event Cancelled",
            message=f"The event '{event.title}' has been cancelled by the organizer.",
            type="EVENT"
        )

    event.delete()
    return Response({
        "status_code": 6000,
        "message": "Event deleted successfully"
    })
