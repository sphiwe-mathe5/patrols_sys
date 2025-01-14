from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import uuid

from django.forms import ValidationError
from submit.managers import CustomUserManager
from django.utils.crypto import get_random_string
from django.utils import timezone

CATEGORY_CHOICES = [
    ('singer', 'Singer'),
    ('dj', 'DJ'),
    ('other', 'Other'),
]
PRICING_CHOICES = [
    ('free', 'Free Trial'),
    ('basic', 'Basic'),
    ('premium', 'Premium'),
]


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, default='none')
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_authorized = models.BooleanField(default=False)
    login_token = models.CharField(max_length=6, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

class PasswordResetRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=32, default=get_random_string(32), editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    TOKEN_VALIDITY_PERIOD = timezone.timedelta(hours=1)

    def is_valid(self):
        return timezone.now() <= self.created_at + self.TOKEN_VALIDITY_PERIOD

    def send_reset_email(self):
        reset_link = f"http://localhost:8000/reset-password/{self.token}/"
        send_mail(
            'Password Reset Request',
            f'Click the following link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )




class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.email} Profile'
