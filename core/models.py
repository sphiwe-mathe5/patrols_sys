from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
import random
from submit.models import Profile, CustomUser
import random
import string


class Resident(models.Model):
    surname = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    place_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentStatus(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    month = models.DateField()  # Will store first day of each month
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['resident', 'month']









