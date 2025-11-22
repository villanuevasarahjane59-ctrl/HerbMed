from django.core.management.base import BaseCommand
from base.models import Herb

class Command(BaseCommand):
    help = 'Populate database with sample herbs using static images'

    def handle(self, *args, **options):
        herbs_data = [
            {
                'name': 'Ginger',
                'scientific_name': 'Zingiber officinale',
                'condition': 'cold',
                'benefits': 'Relieves nausea, supports digestion, boosts immunity',
                'image_url': '/static/base/assets/cold/ginger.webp',
                'procedure': 'Boil fresh ginger slices in water for 10 minutes. Strain and drink warm.',
                'prescription': 'Drink 2-3 cups daily for cold symptoms.',
                'advice': 'Best taken on empty stomach. Add honey for taste.'
            },
            {
                'name': 'Turmeric', 
                'scientific_name': 'Curcuma longa',
                'condition': 'cough',
                'benefits': 'Anti-inflammatory, antioxidant properties, soothes throat',
                'image_url': '/static/base/assets/cough/Turmeric.png',
                'procedure': 'Mix 1 tsp turmeric powder with warm milk or water.',
                'prescription': 'Take twice daily before meals.',
                'advice': 'May stain teeth temporarily. Rinse mouth after use.'
            },
            {
                'name': 'Aloe Vera',
                'scientific_name': 'Aloe barbadensis miller', 
                'condition': 'skin',
                'benefits': 'Promotes healing, hydrates skin, reduces inflammation',
                'image_url': '/static/base/assets/skin allergies/aloe-vera-leaves.png',
                'procedure': 'Extract fresh gel from aloe leaf. Apply directly to affected area.',
                'prescription': 'Apply 2-3 times daily on clean skin.',
                'advice': 'Test on small skin area first. Use fresh gel for best results.'
            },
            {
                'name': 'Lagundi',
                'scientific_name': 'Vitex negundo',
                'condition': 'cough',
                'benefits': 'Natural cough suppressant, anti-inflammatory',
                'image_url': '/static/base/assets/cough/Lagundi-1.jpg',
                'procedure': 'Boil lagundi leaves in water for 15 minutes. Strain.',
                'prescription': 'Drink 1/2 cup 3 times daily.',
                'advice': 'Consult doctor if cough persists beyond 1 week.'
            },
            {
                'name': 'Sambong',
                'scientific_name': 'Blumea balsamifera',
                'condition': 'fever',
                'benefits': 'Reduces fever, diuretic properties, anti-inflammatory',
                'image_url': '/static/base/assets/fever/sambong-removebg-preview (1).png',
                'procedure': 'Boil sambong leaves in water. Let cool and strain.',
                'prescription': 'Drink 1 cup every 4 hours during fever.',
                'advice': 'Monitor temperature regularly. Seek medical help if fever is high.'
            },
            {
                'name': 'Oregano',
                'scientific_name': 'Origanum vulgare',
                'condition': 'cough',
                'benefits': 'Antimicrobial, expectorant, soothes respiratory tract',
                'image_url': '/static/base/assets/cough/Oregano-removebg-preview.png',
                'procedure': 'Steep oregano leaves in hot water for 10 minutes.',
                'prescription': 'Drink as tea 2-3 times daily.',
                'advice': 'Can be combined with honey for better taste and effect.'
            }
        ]
        
        for herb_data in herbs_data:
            herb, created = Herb.objects.get_or_create(
                name=herb_data['name'],
                defaults=herb_data
            )
            if created:
                self.stdout.write(f'Created: {herb.name}')
            else:
                self.stdout.write(f'Already exists: {herb.name}')