from django.db import models

from users.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
        

    def __str__(self):
        return self.user.email


# payments/models.py (or a new file if you prefer)
from django.db import models
from customer.models import Customer
from organizer.models import Event

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        db_table = 'wishlist_table'
        verbose_name = 'wishlist'
        verbose_name_plural = 'wishlists'

    def __str__(self):
        return f"{self.customer} - {self.event}"

class Notification(models.Model):
    TYPE_CHOICES = [
        ("GENERAL", "General"),
        ("BOOKING", "Booking"),
        ("EVENT", "Event"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    type= models.CharField(max_length=20, choices=TYPE_CHOICES, default="GENERAL")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} -> {self.customer.user.username}"



    
    
    
