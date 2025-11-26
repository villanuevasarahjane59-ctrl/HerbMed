import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')
django.setup()

from base.models import Herb

# Clear all uploaded images from database
herbs = Herb.objects.all()
updated_count = 0

for herb in herbs:
    if herb.image or herb.image_url:
        print(f"Clearing images for: {herb.name}")
        print(f"  - Old image: {herb.image}")
        print(f"  - Old image_url: {herb.image_url}")
        
        herb.image = None
        herb.image_url = ''
        herb.save()
        
        print(f"  - New get_image_url(): {herb.get_image_url()}")
        print("---")
        updated_count += 1

print(f"\nSUCCESS: Updated {updated_count} herbs to use hardcoded static images!")
print("All herbs now use static file paths that survive Render restarts.")