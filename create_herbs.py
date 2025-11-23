import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')
django.setup()

from base.models import Herb

# Create sample herbs
herbs_data = [
    {
        'name': 'Ginger',
        'scientific_name': 'Zingiber officinale',
        'condition': 'cold',
        'benefits': 'Relieves nausea, supports digestion, boosts immunity',
        'prescription': 'Ginger tea: Steep 1 tsp fresh ginger in hot water for 10 minutes',
        'advice': 'Take 2-3 times daily. Avoid if you have gallstones.',
        'procedure': '1. Peel and slice fresh ginger\n2. Boil water\n3. Add ginger slices\n4. Steep for 10 minutes\n5. Strain and drink warm',
        'image_url': 'https://picsum.photos/300/300?random=1'
    },
    {
        'name': 'Turmeric',
        'scientific_name': 'Curcuma longa',
        'condition': 'cough',
        'benefits': 'Anti-inflammatory, antioxidant, supports immune system',
        'prescription': 'Golden milk: Mix 1 tsp turmeric powder with warm milk',
        'advice': 'Take before bedtime. May interact with blood thinners.',
        'procedure': '1. Heat milk\n2. Add turmeric powder\n3. Add honey to taste\n4. Stir well\n5. Drink warm',
        'image_url': 'https://picsum.photos/300/300?random=2'
    },
    {
        'name': 'Aloe Vera',
        'scientific_name': 'Aloe barbadensis miller',
        'condition': 'skin',
        'benefits': 'Promotes healing, hydrates skin, soothes inflammation',
        'prescription': 'Apply fresh aloe gel directly to affected skin',
        'advice': 'Use 2-3 times daily. Test on small area first.',
        'procedure': '1. Cut aloe leaf\n2. Extract clear gel\n3. Apply to clean skin\n4. Let absorb naturally\n5. Rinse if sticky',
        'image_url': 'https://picsum.photos/300/300?random=3'
    },
    {
        'name': 'Lemon',
        'scientific_name': 'Citrus limon',
        'condition': 'cold',
        'benefits': 'Rich in vitamin C, boosts immunity, antibacterial',
        'prescription': 'Lemon water: Mix juice of half lemon in warm water',
        'advice': 'Drink on empty stomach. Rinse mouth after to protect teeth.',
        'procedure': '1. Cut lemon in half\n2. Squeeze juice into warm water\n3. Add honey if desired\n4. Stir well\n5. Drink immediately',
        'image_url': 'https://picsum.photos/300/300?random=4'
    },
    {
        'name': 'Garlic',
        'scientific_name': 'Allium sativum',
        'condition': 'cold',
        'benefits': 'Antimicrobial, boosts immunity, reduces inflammation',
        'prescription': 'Crush 2-3 cloves and consume with honey',
        'advice': 'Take with food to avoid stomach upset. May cause bad breath.',
        'procedure': '1. Peel garlic cloves\n2. Crush or chop finely\n3. Mix with honey\n4. Let sit 5 minutes\n5. Consume immediately',
        'image_url': 'https://picsum.photos/300/300?random=5'
    },
    {
        'name': 'Lagundi',
        'scientific_name': 'Vitex negundo',
        'condition': 'cough',
        'benefits': 'Relieves cough, reduces fever, anti-inflammatory',
        'prescription': 'Lagundi tea: Boil 6-8 leaves in 2 cups water',
        'advice': 'Drink 3 times daily. Safe for children over 2 years.',
        'procedure': '1. Wash lagundi leaves\n2. Boil water\n3. Add leaves\n4. Simmer 15 minutes\n5. Strain and drink warm',
        'image_url': 'https://picsum.photos/300/300?random=6'
    },
    {
        'name': 'Sambong',
        'scientific_name': 'Blumea balsamifera',
        'condition': 'fever',
        'benefits': 'Diuretic, anti-inflammatory, reduces fever',
        'prescription': 'Sambong tea: Steep 10-15 leaves in hot water',
        'advice': 'Drink 2-3 times daily. Increase fluid intake.',
        'procedure': '1. Wash sambong leaves\n2. Pour hot water over leaves\n3. Steep 10 minutes\n4. Strain\n5. Drink warm',
        'image_url': 'https://picsum.photos/300/300?random=7'
    }
]

# Create herbs
for herb_data in herbs_data:
    herb, created = Herb.objects.get_or_create(
        name=herb_data['name'],
        defaults=herb_data
    )
    if created:
        print(f'Created: {herb.name}')
    else:
        print(f'Already exists: {herb.name}')

print(f'Total herbs in database: {Herb.objects.count()}')