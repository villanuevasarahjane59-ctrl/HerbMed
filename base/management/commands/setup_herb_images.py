from django.core.management.base import BaseCommand
from base.models import Herb
import base64

class Command(BaseCommand):
    help = 'Setup herb images with Base64 encoding for persistent storage'

    def handle(self, *args, **options):
        # Base64 encoded images (small, optimized herb images)
        herb_images = {
            'ginger': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRkZGNUVFIi8+CjxwYXRoIGQ9Ik0xNTAgNzVDMTc1IDc1IDE5NSA5NSAxOTUgMTIwVjE4MEMxOTUgMjA1IDE3NSAyMjUgMTUwIDIyNUMxMjUgMjI1IDEwNSAyMDUgMTA1IDE4MFYxMjBDMTA1IDk1IDEyNSA3NSAxNTAgNzVaIiBmaWxsPSIjRkZBNTAwIi8+CjxwYXRoIGQ9Ik0xMzAgMTAwQzE0NSAxMDAgMTU3IDExMiAxNTcgMTI3VjE3M0MxNTcgMTg4IDE0NSAyMDAgMTMwIDIwMEMxMTUgMjAwIDEwMyAxODggMTAzIDE3M1YxMjdDMTAzIDExMiAxMTUgMTAwIDEzMCAxMDBaIiBmaWxsPSIjRkY4QzAwIi8+CjxjaXJjbGUgY3g9IjE0MCIgY3k9IjEzMCIgcj0iNSIgZmlsbD0iI0ZGRkZGRiIvPgo8Y2lyY2xlIGN4PSIxNjAiIGN5PSIxNTAiIHI9IjMiIGZpbGw9IiNGRkZGRkYiLz4KPHN2Zz4K',
            
            'turmeric': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRkZGOEVEIi8+CjxwYXRoIGQ9Ik0xNTAgNjBDMTgwIDYwIDIwNSA4NSAyMDUgMTE1VjE4NUMyMDUgMjE1IDE4MCAyNDAgMTUwIDI0MEMxMjAgMjQwIDk1IDIxNSA5NSAxODVWMTE1Qzk1IDg1IDEyMCA2MCAxNTAgNjBaIiBmaWxsPSIjRkZCRjAwIi8+CjxwYXRoIGQ9Ik0xMzUgOTBDMTU1IDkwIDE3MSAxMDYgMTcxIDEyNlYxNzRDMTcxIDE5NCAxNTUgMjEwIDEzNSAyMTBDMTE1IDIxMCA5OSAxOTQgOTkgMTc0VjEyNkM5OSAxMDYgMTE1IDkwIDEzNSA5MFoiIGZpbGw9IiNGRkE1MDAiLz4KPGVsbGlwc2UgY3g9IjE0NSIgY3k9IjEyMCIgcng9IjgiIHJ5PSI0IiBmaWxsPSIjRkZGRkZGIi8+CjxlbGxpcHNlIGN4PSIxNTUiIGN5PSIxNjAiIHJ4PSI2IiByeT0iMyIgZmlsbD0iI0ZGRkZGRiIvPgo8L3N2Zz4K',
            
            'aloe vera': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRjBGRkYwIi8+CjxwYXRoIGQ9Ik0xNTAgNTBMMTIwIDI1MEgxODBMMTUwIDUwWiIgZmlsbD0iIzAwOEIwMCIvPgo8cGF0aCBkPSJNMTUwIDUwTDE4MCAyNTBIMjIwTDE1MCA1MFoiIGZpbGw9IiMwMEFBMDAiLz4KPHN0cm9rZSBkPSJNMTUwIDUwTDgwIDI1MEgxMjBMMTUwIDUwWiIgZmlsbD0iIzAwOEIwMCIvPgo8cGF0aCBkPSJNMTUwIDUwTDIyMCAyNTBIMjYwTDE1MCA1MFoiIGZpbGw9IiMwMDhCMDAiLz4KPHN0cm9rZSBkPSJNMTUwIDUwTDUwIDI1MEg4MEwxNTAgNTBaIiBmaWxsPSIjMDA4QjAwIi8+CjxjaXJjbGUgY3g9IjE0MCIgY3k9IjEyMCIgcj0iMyIgZmlsbD0iI0ZGRkZGRiIvPgo8Y2lyY2xlIGN4PSIxNjAiIGN5PSIxNDAiIHI9IjIiIGZpbGw9IiNGRkZGRkYiLz4KPHN2Zz4K',
            
            'lemon': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRkZGRkY1Ii8+CjxlbGxpcHNlIGN4PSIxNTAiIGN5PSIxNTAiIHJ4PSI2MCIgcnk9IjgwIiBmaWxsPSIjRkZGRjAwIi8+CjxlbGxpcHNlIGN4PSIxNDAiIGN5PSIxNDAiIHJ4PSI0NSIgcnk9IjYwIiBmaWxsPSIjRkZGRjMzIi8+CjxwYXRoIGQ9Ik0xNTAgODBMMTYwIDEwMEwxNzAgODBMMTgwIDEwMEwxOTAgODBMMTgwIDEyMEwxNzAgMTAwTDE2MCA1MDBMMTUwIDgwWiIgZmlsbD0iIzAwOEIwMCIvPgo8Y2lyY2xlIGN4PSIxMzUiIGN5PSIxMzAiIHI9IjMiIGZpbGw9IiNGRkZGRkYiLz4KPGNpcmNsZSBjeD0iMTU1IiBjeT0iMTYwIiByPSIyIiBmaWxsPSIjRkZGRkZGIi8+Cjwvc3ZnPgo=',
            
            'garlic': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRkFGQUZBIi8+CjxjaXJjbGUgY3g9IjE1MCIgY3k9IjE1MCIgcj0iNzAiIGZpbGw9IiNGNUY1RjUiLz4KPGNpcmNsZSBjeD0iMTUwIiBjeT0iMTUwIiByPSI1NSIgZmlsbD0iI0ZGRkZGRiIvPgo8cGF0aCBkPSJNMTUwIDEwMEwxNjAgMTIwTDE3MCA5MEwxODAgMTEwTDE5MCA4MEwxODAgMTMwTDE3MCA5MEwxNjAgMTIwTDE1MCAxMDBaIiBmaWxsPSIjMDA4QjAwIi8+CjxjaXJjbGUgY3g9IjEzNSIgY3k9IjE0MCIgcj0iOCIgZmlsbD0iI0Y1RjVGNSIvPgo8Y2lyY2xlIGN4PSIxNjUiIGN5PSIxNjAiIHI9IjYiIGZpbGw9IiNGNUY1RjUiLz4KPHN2Zz4K',
            
            'lagundi': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRjBGRkYwIi8+CjxwYXRoIGQ9Ik0xNTAgNTBMMTIwIDEwMEw5MCAyMDBMMTIwIDI1MEgxODBMMjEwIDIwMEwxODAgMTAwTDE1MCA1MFoiIGZpbGw9IiMwMDhCMDAiLz4KPHN0cm9rZSBkPSJNMTUwIDUwTDE4MCAyNTBIMjIwTDE5MCAyMDBMMjEwIDEwMEwxNTAgNTBaIiBmaWxsPSIjMDBBQTAwIi8+CjxwYXRoIGQ9Ik0xNTAgNTBMMTIwIDI1MEg4MEwxMTAgMjAwTDkwIDEwMEwxNTAgNTBaIiBmaWxsPSIjMDA4QjAwIi8+CjxjaXJjbGUgY3g9IjE0MCIgY3k9IjEyMCIgcj0iMyIgZmlsbD0iI0ZGRkZGRiIvPgo8Y2lyY2xlIGN4PSIxNjAiIGN5PSIxNDAiIHI9IjIiIGZpbGw9IiNGRkZGRkYiLz4KPHN2Zz4K',
            
            'sambong': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRjVGRkY1Ii8+CjxwYXRoIGQ9Ik0xNTAgNDBMMTMwIDgwTDExMCAxNDBMMTMwIDIwMEwxNTAgMjQwTDE3MCAyMDBMMTkwIDE0MEwxNzAgODBMMTUwIDQwWiIgZmlsbD0iIzIyOEIyMiIvPgo8cGF0aCBkPSJNMTUwIDQwTDE3MCAyNDBIMjAwTDE4MCAyMDBMMjAwIDEwMEwxNTAgNDBaIiBmaWxsPSIjMzNBQTMzIi8+CjxwYXRoIGQ9Ik0xNTAgNDBMMTMwIDI0MEgxMDBMMTIwIDIwMEwxMDAgMTAwTDE1MCA0MFoiIGZpbGw9IiMyMjhCMjIiLz4KPGNpcmNsZSBjeD0iMTQwIiBjeT0iMTEwIiByPSI0IiBmaWxsPSIjRkZGRkZGIi8+CjxjaXJjbGUgY3g9IjE2MCIgY3k9IjEzMCIgcj0iMyIgZmlsbD0iI0ZGRkZGRiIvPgo8L3N2Zz4K'
        }

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
                'name': 'Lagundi',
                'scientific_name': 'Vitex negundo',
                'condition': 'cough',
                'benefits': 'Relieves cough, reduces fever, anti-inflammatory',
                'prescription': 'Lagundi tea: Boil 6-8 leaves in 2 cups water',
                'advice': 'Drink 3 times daily. Safe for children over 2 years.',
                'procedure': '1. Wash lagundi leaves\n2. Boil water\n3. Add leaves\n4. Simmer 15 minutes\n5. Strain and drink warm'
            },
            {
                'name': 'Sambong',
                'scientific_name': 'Blumea balsamifera',
                'condition': 'fever',
                'benefits': 'Diuretic, anti-inflammatory, reduces fever',
                'prescription': 'Sambong tea: Steep 10-15 leaves in hot water',
                'advice': 'Drink 2-3 times daily. Increase fluid intake.',
                'procedure': '1. Wash sambong leaves\n2. Pour hot water over leaves\n3. Steep 10 minutes\n4. Strain\n5. Drink warm'
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
            
            # Set the Base64 image
            if herb_name in herb_images:
                herb.image_url = herb_images[herb_name]
                herb.save()
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created: {herb.name} with image')
                else:
                    updated_count += 1
                    self.stdout.write(f'Updated: {herb.name} with new image')
            else:
                if created:
                    created_count += 1
                    self.stdout.write(f'Created: {herb.name} (no image)')

        self.stdout.write(
            self.style.SUCCESS(
                f'Summary: {created_count} herbs created, {updated_count} herbs updated'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Total herbs in database: {Herb.objects.count()}'
            )
        )