from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    travel_style = models.CharField(
        max_length=50,
        blank=True
    )
    
    preferred_destination = models.CharField(
        max_length=100,
        blank=True
    )
    
    budget_preference = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
