from django.core.management.base import BaseCommand
from base.models import Herb

class Command(BaseCommand):
    help = 'Restore original herb images with proper static paths'

    def handle(self, *args, **options):
        # Original working image mappings
        herb_image_mappings = {
            'ginger': '/static/base/assets/cold/ginger.webp',
            'turmeric': '/static/base/assets/cough/Turmeric.png', 
            'aloe vera': '/static/base/assets/skin allergies/aloe-vera-leaves.png',
            'lemon': '/static/base/assets/cold/lemon (1).png',
            'garlic': '/static/base/assets/cold/garlic.png',
            'onion': '/static/base/assets/cold/onion.png',
            'lagundi': '/static/base/assets/cough/lagundi.png',
            'oregano': '/static/base/assets/cough/oregano.png',
            'sambong': '/static/base/assets/fever/sambong.png',
            'banaba': '/static/base/assets/fever/banaba.png',
        }

        # Complete herb data with original working setup
        herbs_data = [
            {
                'name': 'Ginger',
                'scientific_name': 'Zingiber officinale',
                'condition': 'cold',
                'benefits': 'Relieves nausea, supports digestion, boosts immunity',
                'prescription': 'Ginger tea: Steep 1 tsp fresh ginger in hot water for 10 minutes',
                'advice': 'Take 2-3 times daily. Avoid if you have gallstones.',
                'procedure': '1. Peel and slice fresh ginger\n2. Boil water\n3. Add ginger slices\n4. Steep for 10 minutes\n5. Strain and drink warm'
            },
            {
                'name': 'Turmeric',
                'scientific_name': 'Curcuma longa',
                'condition': 'cough',
                'benefits': 'Anti-inflammatory, antioxidant, supports immune system',
                'prescription': 'Golden milk: Mix 1 tsp turmeric powder with warm milk',
                'advice': 'Take before bedtime. May interact with blood thinners.',
                'procedure': '1. Heat milk\n2. Add turmeric powder\n3. Add honey to taste\n4. Stir well\n5. Drink warm'
            },
            {
                'name': 'Aloe Vera',
                'scientific_name': 'Aloe barbadensis miller',
                'condition': 'skin',
                'benefits': 'Promotes healing, hydrates skin, soothes inflammation',
                'prescription': 'Apply fresh aloe gel directly to affected skin',
                'advice': 'Use 2-3 times daily. Test on small area first.',
                'procedure': '1. Cut aloe leaf\n2. Extract clear gel\n3. Apply to clean skin\n4. Let absorb naturally\n5. Rinse if sticky'
            },
            {
                'name': 'Lemon',
                'scientific_name': 'Citrus limon',
                'condition': 'cold',
                'benefits': 'Rich in vitamin C, boosts immunity, antibacterial',
                'prescription': 'Lemon water: Mix juice of half lemon in warm water',
                'advice': 'Drink on empty stomach. Rinse mouth after to protect teeth.',
                'procedure': '1. Cut lemon in half\n2. Squeeze juice into warm water\n3. Add honey if desired\n4. Stir well\n5. Drink immediately'
            },
            {
                'name': 'Garlic',
                'scientific_name': 'Allium sativum',
                'condition': 'cold',
                'benefits': 'Antimicrobial, boosts immunity, reduces inflammation',
                'prescription': 'Crush 2-3 cloves and consume with honey',
                'advice': 'Take with food to avoid stomach upset. May cause bad breath.',
                'procedure': '1. Peel garlic cloves\n2. Crush or chop finely\n3. Mix with honey\n4. Let sit 5 minutes\n5. Consume immediately'
            },
            {
                'name': 'Onion',
                'scientific_name': 'Allium cepa',
                'condition': 'cold',
                'benefits': 'Natural antibiotic, reduces inflammation, clears congestion',
                'prescription': 'Onion syrup: Layer sliced onions with honey, let sit overnight',
                'advice': 'Take 1 tsp every 2-3 hours. Store in refrigerator.',
                'procedure': '1. Slice onions thinly\n2. Layer with honey in jar\n3. Let sit 8-12 hours\n4. Strain syrup\n5. Take as needed'
            },
            {
                'name': 'Lagundi',
                'scientific_name': 'Vitex negundo',
                'condition': 'cough',
                'benefits': 'Relieves cough, reduces fever, anti-inflammatory',
                'prescription': 'Lagundi tea: Boil 6-8 leaves in 2 cups water',
                'advice': 'Drink 3 times daily. Safe for children over 2 years.',
                'procedure': '1. Wash lagundi leaves\n2. Boil water\n3. Add leaves\n4. Simmer 15 minutes\n5. Strain and drink warm'
            },
            {
                'name': 'Oregano',
                'scientific_name': 'Origanum vulgare',
                'condition': 'cough',
                'benefits': 'Antimicrobial, expectorant, soothes throat',
                'prescription': 'Oregano tea: Steep 1 tsp dried oregano in hot water',
                'advice': 'Drink 2-3 times daily. Add honey for taste.',
                'procedure': '1. Boil water\n2. Add oregano leaves\n3. Steep 10 minutes\n4. Strain\n5. Add honey if desired'
            },
            {
                'name': 'Sambong',
                'scientific_name': 'Blumea balsamifera',
                'condition': 'fever',
                'benefits': 'Diuretic, anti-inflammatory, reduces fever',
                'prescription': 'Sambong tea: Steep 10-15 leaves in hot water',
                'advice': 'Drink 2-3 times daily. Increase fluid intake.',
                'procedure': '1. Wash sambong leaves\n2. Pour hot water over leaves\n3. Steep 10 minutes\n4. Strain\n5. Drink warm'
            },
            {
                'name': 'Banaba',
                'scientific_name': 'Lagerstroemia speciosa',
                'condition': 'fever',
                'benefits': 'Reduces fever, anti-inflammatory, antioxidant',
                'prescription': 'Banaba tea: Boil 8-10 leaves in water',
                'advice': 'Drink 2-3 times daily. Monitor blood sugar if diabetic.',
                'procedure': '1. Wash banaba leaves\n2. Boil in water 15 minutes\n3. Let cool slightly\n4. Strain\n5. Drink warm'
            }
        ]

        created_count = 0
        updated_count = 0

        for herb_data in herbs_data:
            herb_name = herb_data['name'].lower()
            
            herb, created = Herb.objects.get_or_create(
                name=herb_data['name'],
                defaults=herb_data
            )
            
            # Update existing herbs with new data
            if not created:
                for key, value in herb_data.items():
                    setattr(herb, key, value)
            
            # Set the original working image path
            if herb_name in herb_image_mappings:
                herb.image_url = herb_image_mappings[herb_name]
                # Clear any problematic fields
                herb.image_base64 = None
                herb.save()
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created: {herb.name} with original image')
                else:
                    updated_count += 1
                    self.stdout.write(f'Restored: {herb.name} with original image')
            else:
                # Use default image for herbs without specific mapping
                herb.image_url = '/static/base/assets/herbs_292843331-removebg-preview.png'
                herb.image_base64 = None
                herb.save()
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created: {herb.name} with default image')
                else:
                    updated_count += 1
                    self.stdout.write(f'Updated: {herb.name} with default image')

        self.stdout.write(
            self.style.SUCCESS(
                f'Summary: {created_count} herbs created, {updated_count} herbs restored'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Total herbs in database: {Herb.objects.count()}'
            )
        )