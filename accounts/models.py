from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank= True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null= True)
    
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self) -> str:
        return self.name