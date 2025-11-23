from django.core.management.base import BaseCommand
from base.models import Herb

class Command(BaseCommand):
    help = 'Restore herb images by setting proper static paths'

    def handle(self, *args, **options):
        # Define image mappings for common herbs
        herb_images = {
            'ginger': '/static/base/assets/cold/ginger.webp',
            'turmeric': '/static/base/assets/cough/Turmeric.png',
            'aloe vera': '/static/base/assets/skin/aloe-vera-leaves.png',
            'lemon': '/static/base/assets/cold/lemon (1).png',
            'garlic': '/static/base/assets/cold/garlic.webp',
            'onion': '/static/base/assets/cold/Onion.jpg',
            'lagundi': '/static/base/assets/cough/Lagundi-1.jpg',
            'oregano': '/static/base/assets/cough/Oregano.jpg',
            'sambong': '/static/base/assets/fever/sambong.jpg',
            'banaba': '/static/base/assets/fever/banaba.jpg',
            'malunggay': '/static/base/assets/skin/malunggay.png',
            'guava': '/static/base/assets/wound/Guava-Leaf.png',
            'papaya': '/static/base/assets/wound/Papaya-leaf.png',
            'akapulto': '/static/base/assets/skin/akapulto.jpg',
            'ampalaya': '/static/base/assets/fever/ampalaya1.jpg',
            'calamansi': '/static/base/assets/cold/calamansi.png',
            'lemongrass': '/static/base/assets/cold/lemongrass.jpg',
            'yerba buena': '/static/base/assets/cough/yerba_buena.png',
            'tsaang gubat': '/static/base/assets/wound/Tsaang_Gubat.jpg',
        }
        
        herbs = Herb.objects.all()
        updated_count = 0
        
        for herb in herbs:
            herb_name_lower = herb.name.lower()
            
            # Check if we have a specific mapping for this herb
            if herb_name_lower in herb_images:
                herb.image_url = herb_images[herb_name_lower]
                herb.save()
                updated_count += 1
                self.stdout.write(f'✓ Updated {herb.name}: {herb.image_url}')
            else:
                # Generate path based on condition and name
                herb_slug = herb_name_lower.replace(' ', '-').replace('_', '-')
                condition_folder = {
                    'cold': 'cold',
                    'cough': 'cough', 
                    'fever': 'fever',
                    'skin': 'skin',
                    'wound': 'wound'
                }.get(herb.condition, '')
                
                if condition_folder:
                    suggested_path = f'/static/base/assets/{condition_folder}/{herb_slug}.png'
                else:
                    suggested_path = f'/static/base/assets/{herb_slug}.png'
                
                herb.image_url = suggested_path
                herb.save()
                updated_count += 1
                self.stdout.write(f'✓ Generated path for {herb.name}: {suggested_path}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} herbs with image paths')
        )