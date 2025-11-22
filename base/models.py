from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'fullname']

    def __str__(self):
        return self.username


# 🌿 New Model for Herbs
class Herb(models.Model):
    CONDITION_CHOICES = [
        ('cough', 'Cough'),
        ('cold', 'Cold & Flu'),
        ('fever', 'Fever'),
        ('skin', 'Skin Allergy'),
        ('wound', 'Wound Care'),
    ]

    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    image = models.ImageField(upload_to='herbs/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Alternative to image upload - paste image URL")
    benefits = models.TextField(help_text="List benefits separated by commas", blank=True)
    prescription = models.TextField(blank=True)
    advice = models.TextField(blank=True)
    procedure = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    locations = JSONField(default=list)   # [{lat:..., lng:...}, ...]

    created_at = models.DateTimeField(auto_now_add=True)


    def benefit_list(self):
        if self.benefits:
            return [b.strip() for b in self.benefits.split(',')]
        return []

    def get_image_url(self):
        # Prioritize image_url field for production
        if self.image_url and self.image_url.strip():
            return self.image_url.strip()
        elif self.image:
            return self.image.url
        return '/static/base/assets/herbs_292843331-removebg-preview.png'  # default
    
    def __str__(self):
        return f"{self.name} ({self.get_condition_display()})"
        
