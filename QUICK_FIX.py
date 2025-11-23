import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')
django.setup()

from base.models import Herb

# Quick fix - set image URLs for all herbs
herbs = Herb.objects.all()

image_urls = {
    'ginger': 'https://picsum.photos/300/300?random=1',
    'turmeric': 'https://picsum.photos/300/300?random=2', 
    'aloe vera': 'https://picsum.photos/300/300?random=3',
    'lemon': 'https://picsum.photos/300/300?random=4',
    'garlic': 'https://picsum.photos/300/300?random=5',
    'onion': 'https://picsum.photos/300/300?random=6',
    'lagundi': 'https://picsum.photos/300/300?random=7',
    'oregano': 'https://picsum.photos/300/300?random=8',
    'sambong': 'https://picsum.photos/300/300?random=9',
    'banaba': 'https://picsum.photos/300/300?random=10',
}

for herb in herbs:
    herb_name = herb.name.lower()
    if herb_name in image_urls:
        herb.image_url = image_urls[herb_name]
    else:
        herb.image_url = f'https://picsum.photos/300/300?random={herb.pk}'
    herb.save()
    print(f'Updated {herb.name}: {herb.image_url}')

print(f'Fixed {herbs.count()} herbs')