import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')
django.setup()

from base.models import Herb

print("=== HERB IMAGE TEST ===")
print()

for herb in Herb.objects.all()[:3]:  # Test first 3 herbs
    print(f"Herb: {herb.name}")
    print(f"  image_url field: '{herb.image_url}'")
    print(f"  get_image_url(): '{herb.get_image_url()}'")
    
    # Check if file exists
    if herb.image_url and herb.image_url.startswith('/static/'):
        # Convert static URL to file path
        static_path = herb.image_url.replace('/static/', '')
        file_path = f"staticfiles/{static_path}"
        exists = os.path.exists(file_path)
        print(f"  File exists: {exists} ({file_path})")
    
    print()

print("=== TESTING SPECIFIC PATHS ===")
test_paths = [
    "/static/base/assets/herbs/ginger.webp",
    "/static/base/assets/herbs/Turmeric.png",
    "/static/base/assets/herbs/aloe-vera-leaves.png"
]

for path in test_paths:
    static_path = path.replace('/static/', '')
    file_path = f"staticfiles/{static_path}"
    exists = os.path.exists(file_path)
    print(f"{path} -> File exists: {exists}")