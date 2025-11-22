from django.contrib import admin
from .models import CustomUser, Herb

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'fullname', 'is_staff']
    search_fields = ['username', 'email', 'fullname']

@admin.register(Herb)
class HerbAdmin(admin.ModelAdmin):
    list_display = ['name', 'condition', 'scientific_name', 'created_at', 'has_image']
    list_filter = ['condition', 'created_at']
    search_fields = ['name', 'scientific_name']
    readonly_fields = ['created_at']
    
    def has_image(self, obj):
        return bool(obj.image or obj.image_url)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
