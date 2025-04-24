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


class Farm(models.Model):
    name = models.CharField(max_length=100)

class Field(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Crop(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    harvest_date = models.DateField()

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    assigned_farm = models.ForeignKey(Farm, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_field = models.ForeignKey(Field, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20)
