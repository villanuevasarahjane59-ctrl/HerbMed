from django.core.management.base import BaseCommand
from base.models import Herb
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Fix herb images by setting proper static paths or clearing broken references'

    def handle(self, *args, **options):
        herbs = Herb.objects.all()
        fixed_count = 0
        
        for herb in herbs:
            updated = False
            
            # If herb has an uploaded image but no image_url, try to set a static path
            if herb.image and not herb.image_url:
                # Try to find a matching static file
                herb_name = herb.name.lower().replace(" ", "-").replace("_", "-")
                
                # Common static paths to try
                static_paths = [
                    f'/static/base/assets/{herb_name}.png',
                    f'/static/base/assets/{herb_name}.jpg',
                    f'/static/base/assets/{herb_name}.webp',
                    f'/static/base/assets/cold/{herb_name}.webp',
                    f'/static/base/assets/cough/{herb_name}.png',
                    f'/static/base/assets/fever/{herb_name}.png',
                    f'/static/base/assets/skin/{herb_name}.png',
                    f'/static/base/assets/wound/{herb_name}.png',
                ]
                
                # Set the first potential path (browser will handle 404s)
                herb.image_url = static_paths[0]
                updated = True
                self.stdout.write(f'Set static path for {herb.name}: {herb.image_url}')
            
            # Clear broken image field references (they won't work on Render anyway)
            if herb.image:
                try:
                    # Try to access the file
                    if not os.path.exists(herb.image.path):
                        herb.image = None
                        updated = True
                        self.stdout.write(f'Cleared broken image reference for {herb.name}')
                except (ValueError, AttributeError):
                    herb.image = None
                    updated = True
                    self.stdout.write(f'Cleared invalid image reference for {herb.name}')
            
            if updated:
                herb.save()
                fixed_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} herbs')
        )