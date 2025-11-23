import os
import base64
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')
django.setup()

from base.models import Herb

# Create directory for extracted images
output_dir = 'extracted_herb_images'
os.makedirs(output_dir, exist_ok=True)

herbs = Herb.objects.all()

for herb in herbs:
    if herb.image_url and herb.image_url.startswith('data:image/svg+xml;base64,'):
        # Extract Base64 data
        base64_data = herb.image_url.split(',')[1]
        
        # Decode Base64 to SVG
        svg_content = base64.b64decode(base64_data).decode('utf-8')
        
        # Save as SVG file
        filename = f"{herb.name.lower().replace(' ', '_')}.svg"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f'Extracted: {filename}')

print(f'\nAll images extracted to: {output_dir}/')
print('You can now convert these SVG files to PNG/JPG using any image editor.')