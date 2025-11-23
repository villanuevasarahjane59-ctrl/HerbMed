from django.core.management.base import BaseCommand
from base.models import Herb

class Command(BaseCommand):
    help = 'Create sample herbs if none exist'

    def handle(self, *args, **options):
        if Herb.objects.exists():
            self.stdout.write('Herbs already exist, skipping...')
            return

        herbs_data = [
            {
                'name': 'Ginger',
                'scientific_name': 'Zingiber officinale',
                'condition': 'cold',
                'benefits': 'Relieves nausea, supports digestion, boosts immunity',
                'image_url': 'https://picsum.photos/300/300?random=1'
            },
            {
                'name': 'Turmeric',
                'scientific_name': 'Curcuma longa',
                'condition': 'cough',
                'benefits': 'Anti-inflammatory, antioxidant, supports immune system',
                'image_url': 'https://picsum.photos/300/300?random=2'
            },
            # Add other herbs...
        ]

        for herb_data in herbs_data:
            Herb.objects.create(**herb_data)
            
        self.stdout.write(f'Created {len(herbs_data)} herbs')