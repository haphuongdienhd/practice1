from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import MyUserManager

class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    signup_token = models.CharField(max_length=50, unique=True, null=True)
    signup_token_created = models.DateTimeField(null=True)
    
    objects = MyUserManager()
    
    def __str__(self):
        return self.username