from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class Destination(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="destinations"
    )
    image = models.ImageField(
        upload_to="destinations/",
        blank=True,
        null=True
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.name}, {self.country}"