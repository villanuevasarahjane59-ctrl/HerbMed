from django.core.management.base import BaseCommand
from base.models import Herb
from django.core.files.base import ContentFile
import requests
import uuid
import os

class Command(BaseCommand):
    help = 'Fix duplicate herb images by ensuring each herb has a unique image'

    def handle(self, *args, **options):
        herbs = Herb.objects.all()
        
        # Group herbs by their current image path
        image_groups = {}
        for herb in herbs:
            if herb.image:
                image_path = str(herb.image)
                if image_path not in image_groups:
                    image_groups[image_path] = []
                image_groups[image_path].append(herb)
        
        fixed_count = 0
        
        for image_path, herb_list in image_groups.items():
            if len(herb_list) > 1:  # Multiple herbs using same image
                self.stdout.write(f'Found {len(herb_list)} herbs using same image: {image_path}')
                
                # Keep the first herb with the original image
                original_herb = herb_list[0]
                
                # For other herbs, create copies with unique names
                for i, herb in enumerate(herb_list[1:], 1):
                    try:
                        # Get the original image file
                        original_image = original_herb.image
                        if original_image and os.path.exists(original_image.path):
                            # Read the image content
                            with open(original_image.path, 'rb') as f:
                                image_content = f.read()
                            
                            # Create new unique filename
                            ext = image_path.split('.')[-1]
                            new_filename = f"{uuid.uuid4().hex}_{herb.name.replace(' ', '_')}.{ext}"
                            
                            # Save as new file
                            herb.image.save(
                                new_filename,
                                ContentFile(image_content),
                                save=True
                            )
                            
                            fixed_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'Fixed image for herb: {herb.name} -> {new_filename}')
                            )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error fixing herb {herb.name}: {str(e)}')
                        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} duplicate herb images')
        )