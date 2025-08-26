from django.db import models
from users.models import User
from organizer.models import Event
import uuid



class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    tickets_count = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    qr_code = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    
    class Meta:
        db_table='booking_table'
        verbose_name='booking'
        verbose_name_plural='bookings'
        ordering =['-id']



    def __str__(self):
            return f"{self.user.username} - {self.event.title} ({self.tickets_count}"



class Payment(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50)  
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    receipt_url = models.URLField(blank=True) 




    class Meta:
        db_table='payment_table'
        verbose_name='payment'
        verbose_name_plural='payments'
        ordering =['-id']

    def __str__(self):
        return f"{self.booking.user.username} - {self.status}"