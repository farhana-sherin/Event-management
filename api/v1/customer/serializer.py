from rest_framework import serializers
from customer.models import Customer
from users.models import User
from payments.models import *
from api.v1.organizer.serializer import *



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user']

class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = Booking
        
        fields = [
            "id","customer","event","tickets_count","total_amount","status","qr_code","created_at"]


class WishlistSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'event', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "title", "message", "is_read", "created_at"]

class PaymentSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source="booking.id", read_only=True)
  

    class Meta:
        model = Payment
        fields = [
            "id",
            "booking_id",
            "provider",
            "payment_id",
            "status",
            "amount",
            "receipt_url",
            
        ]

        
