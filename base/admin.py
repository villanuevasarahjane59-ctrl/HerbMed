from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from .models import Herb, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'fullname', 'is_staff']
    search_fields = ['username', 'email', 'fullname']

@admin.register(Herb)
class HerbAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'condition', 'image_preview', 'created_at']
    list_filter = ['condition', 'created_at']
    search_fields = ['name', 'scientific_name']
    readonly_fields = ['created_at', 'image_preview']
    
    def image_preview(self, obj):
        from django.utils.html import format_html
        return format_html(
            '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
            obj.get_image_url()
        )
    image_preview.short_description = 'Image Preview'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('fix-images/', self.fix_images_view, name='fix_herb_images'),
        ]
        return custom_urls + urls
    
    def fix_images_view(self, request):
        if request.method == 'POST':
            herbs = Herb.objects.all()
            updated_count = 0
            
            for herb in herbs:
                if herb.image or herb.image_url:
                    herb.image = None
                    herb.image_url = ''
                    herb.save()
                    updated_count += 1
            
            self.message_user(request, f'Successfully updated {updated_count} herbs to use hardcoded static images!')
            return HttpResponseRedirect('../')
        
        return render(request, 'admin/fix_images.html', {
            'title': 'Fix Herb Images',
            'herb_count': Herb.objects.count()
        })

    change_list_template = 'admin/herb_changelist.html'