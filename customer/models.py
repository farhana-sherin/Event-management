from django.db import models

from users.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
        

    def __str__(self):
        return self.user.email
    
    
    
