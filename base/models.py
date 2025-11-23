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
        # Priority 1: Image URL field (external links or static paths)
        if self.image_url and self.image_url.strip():
            url = self.image_url.strip()
            # If it's already a full URL or static path, return as is
            if url.startswith(('http://', 'https://', '/static/', '/media/')):
                return url
            # If it's just a filename, try to find it in static assets
            return f'/static/base/assets/{url}'
        
        # Priority 2: Base64 image (persistent on Render)
        if self.image_base64:
            return f'data:image/png;base64,{self.image_base64}'
        
        # Priority 3: Try uploaded image (but will fail on Render after restart)
        if self.image:
            try:
                # Check if file actually exists
                if hasattr(self.image, 'url') and self.image.url:
                    return self.image.url
            except (ValueError, AttributeError, FileNotFoundError):
                pass
        
        # Priority 4: Try to find static image based on herb name
        if self.name:
            # Try most common naming pattern first
            herb_name = self.name.lower().replace(" ", "-").replace("_", "-")
            return f'/static/base/assets/{herb_name}.png'
        
        # Fallback: Default image
        return '/static/base/assets/herbs_292843331-removebg-preview.png'
    
    def __str__(self):
        return f"{self.name} ({self.get_condition_display()})"
        
