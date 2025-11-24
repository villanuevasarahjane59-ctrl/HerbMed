from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField
import uuid
import os

def herb_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}_{instance.name.replace(' ', '_')}.{ext}"
    return f'herbs/{filename}'

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
    image = models.ImageField(upload_to=herb_image_path, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Alternative to image upload - paste image URL")
    image_base64 = models.TextField(blank=True, null=True, help_text="Base64 encoded image data")
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
        # Direct static path mapping for each herb
        herb_images = {
            'ginger': '/static/base/assets/herbs/ginger.webp',
            'turmeric': '/static/base/assets/herbs/Turmeric.png',
            'aloe vera': '/static/base/assets/herbs/aloe-vera-leaves.png',
            'lemon': '/static/base/assets/herbs/lemon (1).png',
            'garlic': '/static/base/assets/herbs/garlic.webp',
            'onion': '/static/base/assets/herbs/Onion-removebg-preview.png',
            'lagundi': '/static/base/assets/herbs/lagundi1.webp',
            'oregano': '/static/base/assets/herbs/Oregano-removebg-preview.png',
            'sambong': '/static/base/assets/herbs/sambong-removebg-preview (1).png',
            'banaba': '/static/base/assets/herbs/banaba1-removebg-preview.png'
        }
        
        # Use direct mapping first
        herb_name = self.name.lower()
        if herb_name in herb_images:
            return herb_images[herb_name]
        
        # Fallback to image_url field
        if self.image_url and self.image_url.strip():
            return self.image_url.strip()
        
        # Final fallback
        return '/static/base/assets/herbs_292843331-removebg-preview.png'
    
    def __str__(self):
        return f"{self.name} ({self.get_condition_display()})"
        
