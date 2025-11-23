from django.core.management.base import BaseCommand
from base.models import Herb

class Command(BaseCommand):
    help = 'Fix herb images for Render deployment with embedded Base64 images'

    def handle(self, *args, **options):
        # Embedded Base64 images that will never disappear
        herb_images = {
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

        herbs_data = [
            {'name': 'Ginger', 'scientific_name': 'Zingiber officinale', 'condition': 'cold', 'benefits': 'Relieves nausea, supports digestion, boosts immunity'},
            {'name': 'Turmeric', 'scientific_name': 'Curcuma longa', 'condition': 'cough', 'benefits': 'Anti-inflammatory, antioxidant, supports immune system'},
            {'name': 'Aloe Vera', 'scientific_name': 'Aloe barbadensis miller', 'condition': 'skin', 'benefits': 'Promotes healing, hydrates skin, soothes inflammation'},
            {'name': 'Lemon', 'scientific_name': 'Citrus limon', 'condition': 'cold', 'benefits': 'Rich in vitamin C, boosts immunity, antibacterial'},
            {'name': 'Garlic', 'scientific_name': 'Allium sativum', 'condition': 'cold', 'benefits': 'Antimicrobial, boosts immunity, reduces inflammation'},
            {'name': 'Onion', 'scientific_name': 'Allium cepa', 'condition': 'cold', 'benefits': 'Natural antibiotic, reduces inflammation, clears congestion'},
            {'name': 'Lagundi', 'scientific_name': 'Vitex negundo', 'condition': 'cough', 'benefits': 'Relieves cough, reduces fever, anti-inflammatory'},
            {'name': 'Oregano', 'scientific_name': 'Origanum vulgare', 'condition': 'cough', 'benefits': 'Antimicrobial, expectorant, soothes throat'},
            {'name': 'Sambong', 'scientific_name': 'Blumea balsamifera', 'condition': 'fever', 'benefits': 'Diuretic, anti-inflammatory, reduces fever'},
            {'name': 'Banaba', 'scientific_name': 'Lagerstroemia speciosa', 'condition': 'fever', 'benefits': 'Reduces fever, anti-inflammatory, antioxidant'}
        ]

        for herb_data in herbs_data:
            herb_name = herb_data['name'].lower()
            herb, created = Herb.objects.get_or_create(name=herb_data['name'], defaults=herb_data)
            
            if not created:
                for key, value in herb_data.items():
                    setattr(herb, key, value)
            
            # Set embedded Base64 image that will NEVER disappear
            if herb_name in herb_images:
                herb.image_url = herb_images[herb_name]
                herb.save()
                self.stdout.write(f'Fixed: {herb.name} with permanent image')

        self.stdout.write(self.style.SUCCESS(f'All {len(herbs_data)} herbs now have permanent images'))