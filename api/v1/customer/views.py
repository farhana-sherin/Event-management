
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.contrib.auth import authenticate ,login as auth_login, logout as auth_logout
from users.models import User
from customer.models import *
from organizer.models import*
from api.v1.organizer.serializer import *
from api.v1.customer.serializer import *



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment(request,id):
   
    user = request.user
    booking = Booking.objects.filter(id=id, customer__user=user).first()
    if not booking:
        return Response({"status_code": 6001, "message": "Booking not found"})

    if booking.status == "PAID":
        payment = Payment.objects.filter(booking=booking).first()
        serializer = PaymentSerializer(payment, context={"request": request})
        
        return Response({"status_code": 6002, "message": "Booking already paid"})

    amount = int(booking.total_amount * 100)  

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='inr',
        metadata={
            "booking_id": booking.id,
            "customer_email": user.email
        },
    )

    return Response({
        "status_code": 6000,
        "data": {
            "client_secret": payment_intent.client_secret,
                "payment_intent_id": payment_intent.id,
                "amount": booking.total_amount
        },
        "message": "Payment initiated successfully"
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_payment(request, id):
    user = request.user
    booking = Booking.objects.filter(id=id, customer__user=user).first()

    if not booking:
        return Response({
            "status_code": 6001, 
            "data": {},
            "message": "Booking not found"
        })

    if booking.status == "PAID":
        payment = Payment.objects.filter(booking=booking).first()
        serializer = PaymentSerializer(payment, context={"request": request})
        return Response({
            "status_code": 6002, 
            "data": serializer.data if payment else {},
            "message": "Booking already paid"
        })

 
    booking.status = "PAID"
    booking.save()

   
    payment, created = Payment.objects.update_or_create(
        booking=booking,
        defaults={
            "customer": booking.customer,
            "provider": "Stripe",
            "payment_id": f"STRIPE-{booking.id}-{booking.qr_code}",
            "status": "SUCCESS",
            "amount": booking.total_amount,
            "receipt_url": "",
        }
    )

    serializer = PaymentSerializer(payment, context={"request": request})

    return Response({
        "status_code": 6000,
        "data": serializer.data,
        "message": "Payment confirmed and booking marked as PAID"
    })

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
            
            
        },
        "message": "Registration successful "
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
   
    response_data={
        "status_code": 6000,
        "message": "Logout successful."
    }


    return Response(response_data)


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
def search_events(request):
   
    keyword = request.data.get("keyword", "")
    category = request.data.get("category", "")
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    events = Event.objects.all()

    if keyword:
        events = events.filter(title__icontains=keyword)

    if category:
        events = events.filter(category__icontains=category)

    if start_date and end_date:
        events = events.filter(start_at__date__range=[start_date, end_date])

    serializer = EventSerializer(events, many=True, context={"request": request})
    return Response({
        "status_code": 6000,
        "data": serializer.data,
        "message": "Search results retrieved successfully"
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_list(request):
    events=Event.objects.all().order_by('-start_at') 
    serializer = EventSerializer(events, many=True, context=
    {'request': request}
    )


    response_data={
        "status_code":6000,
        "data":
            serializer.data,
        "message":"Events retrieved successfully"
    }

    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_detail(request, id):
   
    event = Event.objects.filter(id=id).first()
    if not event:
        return Response({"error": "Event not found"}, status=404)

    serializer = EventSerializer(event, context={"request": request})
    return Response({
        "status_code": 6000,
        "data": serializer.data,
        "message": "Event details retrieved successfully"
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    tickets_count = int(request.data.get("tickets_count", 1))
    context={
        "request":request
    }

  
    event = Event.objects.get(id=id)

    if Booking.objects.filter(customer=customer, event=event).exists():
        return Response({"error": "You already booked this event"})

   
    if event.available_seats < tickets_count:
        return Response({"error": "Not enough seats available"})

   
    booking = Booking.objects.create(
        customer=customer,
        event=event,
        tickets_count=tickets_count,
        total_amount=event.price * tickets_count,
        qr_code=get_random_string(10).upper(),
    )


    event.available_seats -= tickets_count
    event.save()

    response_data = {
        "status_code": 6000,
        "data": BookingSerializer(booking,context=context).data
    }

    return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)

    booking = Booking.objects.filter(id=id, customer=customer).first()

    if not booking:
        return Response({"error": "Booking not found"})

    if booking.status == "CANCELLED":
        return Response({"error": "Booking already cancelled"})

 
    booking.event.available_seats += booking.tickets_count
    booking.event.save()

    
    booking.status = "CANCELLED"
    booking.save()

    response_data = {
        "status_code": 6000,
        "data": BookingSerializer(booking, context={"request": request}).data,
        "message": "Booking cancelled successfully"
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def View_all_booking(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    
    booking=Booking.objects.filter(customer=customer).select_related("event")
    context={
        'request':request
    }
    serializer=BookingSerializer(booking,many=True,context=context)
    


    response_data = {
        "status_code": 6000,
        "data": serializer.data,
        "message": "My tickets retrieved successfully "
    }
    return Response(response_data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_wish_list(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    event = Event.objects.get(id=id)

    context = {
        "request": request
    }

    
    wishlist = Wishlist.objects.filter(customer=customer, event=event).first()
    if wishlist:
       
        wishlist.delete()
        response_data = {
            "status_code": 6000,
            "data": {},
            "message": "Removed from wishlist"
        }
    else:
      
        wishlist = Wishlist.objects.create(customer=customer, event=event)
        serializer = WishlistSerializer(wishlist, context=context)
        response_data = {
            "status_code": 6000,
            "data": serializer.data,
            "message": "Added to wishlist"
        }

    return Response(response_data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    
    wishlist_item = Wishlist.objects.filter(customer=customer, id=id).first()

    if wishlist_item:
       
        serializer = WishlistSerializer(wishlist_item, context={"request": request})
        data = serializer.data  

        wishlist_item.delete()

        response_data = {
            "status_code": 6000,
            "data": data,   
            "message": "Removed from wishlist"
        }
        return Response(response_data)
    else:
        response_data = {
            "error": "Event not in wishlist"
        }
        return Response(response_data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_wishlist(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    context={
        "request":request
    }
    wishlist_items = Wishlist.objects.filter(customer=customer).select_related("event")
    serializer = WishlistSerializer(wishlist_items, many=True,context=context)
    response_data={
        "status_code":6000,
        "data":serializer.data,
        "message":"Wishlist retrieved"
    }

    return Response(response_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    notifications = Notification.objects.filter(customer=customer).order_by("-created_at")

    serializer = NotificationSerializer(notifications, many=True, context={"request": request})

    response_data = {
        "status_code": 6000,
        "data": serializer.data,
        "message": "Notifications retrieved successfully"
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification_detail(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)

    notification = Notification.objects.filter(id=id, customer=customer).first()
    if not notification:
        return Response({"error": "Notification not found"})

    serializer = NotificationSerializer(notification, context={"request": request})
    
    response_data = {
        "status_code": 6000,
        "data": serializer.data,
        "message": "Notification retrieved successfully"
    }
    return Response(response_data)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, id):
    
    user = request.user
    customer = Customer.objects.get(user=user)

    notification = Notification.objects.filter(id=id, customer=customer).first()
    if not notification:
        return Response({"error": "Notification not found"})

    if notification.is_read:
        return Response({"message": "Notification already marked as read"})

    notification.is_read = True
    notification.save()

    response_data = {
        "status_code": 6000,
        "data": NotificationSerializer(notification, context={"request": request}).data,
        "message": "Notification marked as read"
    }
    return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
   
    user = request.user
    customer = Customer.objects.get(user=user)

    updated_count = Notification.objects.filter(customer=customer, is_read=False).update(is_read=True)

    response_data = {
        "status_code": 6000,
        "message": f"{updated_count} notifications marked as read"
    }
    return Response(response_data)




























    





    



