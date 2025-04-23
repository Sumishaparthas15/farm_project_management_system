from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('farm_manager', 'Farm Manager'),
        ('field_worker', 'Field Worker'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20 ,choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

