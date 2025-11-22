from django.core.management.base import BaseCommand
from base.models import Herb
import uuid
import os

class Command(BaseCommand):
    help = 'Fix herb images to ensure unique filenames'

    def handle(self, *args, **options):
        herbs = Herb.objects.all()
        fixed_count = 0
        
        for herb in herbs:
            if herb.image:
                # Get the current image path
                old_path = herb.image.path
                if os.path.exists(old_path):
                    # Generate new unique filename
                    ext = herb.image.name.split('.')[-1]
                    new_filename = f"{uuid.uuid4().hex}_{herb.name.replace(' ', '_')}.{ext}"
                    new_path = os.path.join('herbs', new_filename)
                    
                    # Update the image field
                    herb.image.name = new_path
                    herb.save()
                    fixed_count += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Fixed image for herb: {herb.name}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} herb images')
        )