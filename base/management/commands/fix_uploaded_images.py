from django.core.management.base import BaseCommand
from base.models import Herb

class Command(BaseCommand):
    help = 'Fix uploaded images that get deleted on Render restarts'

    def handle(self, *args, **options):
        # Static image mappings for herbs
        static_images = {
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

        fixed_count = 0
        
        for herb in Herb.objects.all():
            needs_fix = False
            herb_name = herb.name.lower()
            
            # Check if image field points to deleted media file
            if herb.image and str(herb.image).startswith('herbs/'):
                herb.image = None  # Clear broken uploaded image
                needs_fix = True
            
            # Set static image URL if available
            if herb_name in static_images:
                herb.image_url = static_images[herb_name]
                needs_fix = True
            elif not herb.image_url or herb.image_url.startswith('/media/'):
                # If no static mapping, use default
                herb.image_url = '/static/base/assets/herbs_292843331-removebg-preview.png'
                needs_fix = True
            
            if needs_fix:
                herb.save()
                fixed_count += 1
                self.stdout.write(f'Fixed: {herb.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed_count} herbs with permanent images'))