from django.core.management.base import BaseCommand
from base.models import Herb

class Command(BaseCommand):
    help = 'Fix herb images for Render deployment with embedded Base64 images'

    def handle(self, *args, **options):
        # Embedded Base64 images that will never disappear
        herb_images = {
            'ginger': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGRkY1RUUiLz48cGF0aCBkPSJNMTUwIDc1QzE3NSA3NSAxOTUgOTUgMTk1IDEyMFYxODBDMTk1IDIwNSAxNzUgMjI1IDE1MCAyMjVDMTI1IDIyNSAxMDUgMjA1IDEwNSAxODBWMTIwQzEwNSA5NSAxMjUgNzUgMTUwIDc1WiIgZmlsbD0iI0ZGQTUwMCIvPjxwYXRoIGQ9Ik0xMzAgMTAwQzE0NSAxMDAgMTU3IDExMiAxNTcgMTI3VjE3M0MxNTcgMTg4IDE0NSAyMDAgMTMwIDIwMEMxMTUgMjAwIDEwMyAxODggMTAzIDE3M1YxMjdDMTAzIDExMiAxMTUgMTAwIDEzMCAxMDBaIiBmaWxsPSIjRkY4QzAwIi8+PGNpcmNsZSBjeD0iMTQwIiBjeT0iMTMwIiByPSI1IiBmaWxsPSIjRkZGRkZGIi8+PGNpcmNsZSBjeD0iMTYwIiBjeT0iMTUwIiByPSIzIiBmaWxsPSIjRkZGRkZGIi8+PC9zdmc+',
            'turmeric': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGRkY4RUQiLz48cGF0aCBkPSJNMTUwIDYwQzE4MCA2MCAyMDUgODUgMjA1IDExNVYxODVDMjA1IDIxNSAxODAgMjQwIDE1MCAyNDBDMTIwIDI0MCA5NSAyMTUgOTUgMTg1VjExNUM5NSA4NSAxMjAgNjAgMTUwIDYwWiIgZmlsbD0iI0ZGQkYwMCIvPjxwYXRoIGQ9Ik0xMzUgOTBDMTU1IDkwIDE3MSAxMDYgMTcxIDEyNlYxNzRDMTcxIDE5NCAxNTUgMjEwIDEzNSAyMTBDMTE1IDIxMCA5OSAxOTQgOTkgMTc0VjEyNkM5OSAxMDYgMTE1IDkwIDEzNSA5MFoiIGZpbGw9IiNGRkE1MDAiLz48ZWxsaXBzZSBjeD0iMTQ1IiBjeT0iMTIwIiByeD0iOCIgcnk9IjQiIGZpbGw9IiNGRkZGRkYiLz48ZWxsaXBzZSBjeD0iMTU1IiBjeT0iMTYwIiByeD0iNiIgcnk9IjMiIGZpbGw9IiNGRkZGRkYiLz48L3N2Zz4=',
            'aloe vera': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGMEZGRjAiLz48cGF0aCBkPSJNMTUwIDUwTDEyMCAyNTBIMTgwTDE1MCA1MFoiIGZpbGw9IiMwMDhCMDAiLz48cGF0aCBkPSJNMTUwIDUwTDE4MCAyNTBIMjIwTDE1MCA1MFoiIGZpbGw9IiMwMEFBMDAiLz48cGF0aCBkPSJNMTUwIDUwTDgwIDI1MEgxMjBMMTUwIDUwWiIgZmlsbD0iIzAwOEIwMCIvPjxwYXRoIGQ9Ik0xNTAgNTBMMjIwIDI1MEgyNjBMMTUwIDUwWiIgZmlsbD0iIzAwOEIwMCIvPjxwYXRoIGQ9Ik0xNTAgNTBMNTAgMjUwSDgwTDE1MCA1MFoiIGZpbGw9IiMwMDhCMDAiLz48Y2lyY2xlIGN4PSIxNDAiIGN5PSIxMjAiIHI9IjMiIGZpbGw9IiNGRkZGRkYiLz48Y2lyY2xlIGN4PSIxNjAiIGN5PSIxNDAiIHI9IjIiIGZpbGw9IiNGRkZGRkYiLz48L3N2Zz4=',
            'lemon': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGRkZGRjUiLz48ZWxsaXBzZSBjeD0iMTUwIiBjeT0iMTUwIiByeD0iNjAiIHJ5PSI4MCIgZmlsbD0iI0ZGRkYwMCIvPjxlbGxpcHNlIGN4PSIxNDAiIGN5PSIxNDAiIHJ4PSI0NSIgcnk9IjYwIiBmaWxsPSIjRkZGRjMzIi8+PHBhdGggZD0iTTE1MCA4MEwxNjAgMTAwTDE3MCA4MEwxODAgMTAwTDE5MCA4MEwxODAgMTIwTDE3MCAxMDBMMTYwIDEyMEwxNTAgODBaIiBmaWxsPSIjMDA4QjAwIi8+PGNpcmNsZSBjeD0iMTM1IiBjeT0iMTMwIiByPSIzIiBmaWxsPSIjRkZGRkZGIi8+PGNpcmNsZSBjeD0iMTU1IiBjeT0iMTYwIiByPSIyIiBmaWxsPSIjRkZGRkZGIi8+PC9zdmc+',
            'garlic': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGQUZBRkEiLz48Y2lyY2xlIGN4PSIxNTAiIGN5PSIxNTAiIHI9IjcwIiBmaWxsPSIjRjVGNUY1Ii8+PGNpcmNsZSBjeD0iMTUwIiBjeT0iMTUwIiByPSI1NSIgZmlsbD0iI0ZGRkZGRiIvPjxwYXRoIGQ9Ik0xNTAgMTAwTDE2MCAxMjBMMTcwIDkwTDE4MCAxMTBMMTkwIDgwTDE4MCAxMzBMMTcwIDkwTDE2MCAxMjBMMTUwIDEwMFoiIGZpbGw9IiMwMDhCMDAiLz48Y2lyY2xlIGN4PSIxMzUiIGN5PSIxNDAiIHI9IjgiIGZpbGw9IiNGNUY1RjUiLz48Y2lyY2xlIGN4PSIxNjUiIGN5PSIxNjAiIHI9IjYiIGZpbGw9IiNGNUY1RjUiLz48L3N2Zz4=',
            'onion': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGRkY4RjAiLz48ZWxsaXBzZSBjeD0iMTUwIiBjeT0iMTcwIiByeD0iNzAiIHJ5PSI5MCIgZmlsbD0iI0ZGRkZGRiIvPjxlbGxpcHNlIGN4PSIxNTAiIGN5PSIxNzAiIHJ4PSI1NSIgcnk9IjcwIiBmaWxsPSIjRkZGNUY1Ii8+PGVsbGlwc2UgY3g9IjE1MCIgY3k9IjE3MCIgcng9IjQwIiByeT0iNTAiIGZpbGw9IiNGRkVERUQiLz48cGF0aCBkPSJNMTUwIDgwTDE2MCA5MEwxNzAgODBMMTgwIDkwTDE5MCA4MEwxODAgMTEwTDE3MCA5MEwxNjAgMTEwTDE1MCA4MFoiIGZpbGw9IiMwMDhCMDAiLz48L3N2Zz4=',
            'lagundi': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGMEZGRjAiLz48cGF0aCBkPSJNMTUwIDUwTDEyMCAxMDBMOTAgMjAwTDEyMCAyNTBIMTgwTDIxMCAyMDBMMTgwIDEwMEwxNTAgNTBaIiBmaWxsPSIjMDA4QjAwIi8+PHBhdGggZD0iTTE1MCA1MEwxODAgMjUwSDIyMEwxOTAgMjAwTDIxMCAxMDBMMTUwIDUwWiIgZmlsbD0iIzAwQUEwMCIvPjxwYXRoIGQ9Ik0xNTAgNTBMMTIwIDI1MEg4MEwxMTAgMjAwTDkwIDEwMEwxNTAgNTBaIiBmaWxsPSIjMDA4QjAwIi8+PGNpcmNsZSBjeD0iMTQwIiBjeT0iMTIwIiByPSIzIiBmaWxsPSIjRkZGRkZGIi8+PGNpcmNsZSBjeD0iMTYwIiBjeT0iMTQwIiByPSIyIiBmaWxsPSIjRkZGRkZGIi8+PC9zdmc+',
            'oregano': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGNUZGRjUiLz48cGF0aCBkPSJNMTUwIDUwTDEzMCAxMDBMMTEwIDE2MEwxMzAgMjIwTDE1MCAyNTBMMTcwIDIyMEwxOTAgMTYwTDE3MCAxMDBMMTUwIDUwWiIgZmlsbD0iIzIyOEIyMiIvPjxwYXRoIGQ9Ik0xNTAgNTBMMTcwIDI1MEgyMDBMMTgwIDIyMEwyMDAgMTIwTDE1MCA1MFoiIGZpbGw9IiMzM0FBMzMiLz48cGF0aCBkPSJNMTUwIDUwTDEzMCAyNTBIMTAwTDEyMCAyMjBMMTAwIDEyMEwxNTAgNTBaIiBmaWxsPSIjMjI4QjIyIi8+PGNpcmNsZSBjeD0iMTQwIiBjeT0iMTEwIiByPSI0IiBmaWxsPSIjRkZGRkZGIi8+PGNpcmNsZSBjeD0iMTYwIiBjeT0iMTMwIiByPSIzIiBmaWxsPSIjRkZGRkZGIi8+PC9zdmc+',
            'sambong': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGNUZGRjUiLz48cGF0aCBkPSJNMTUwIDQwTDEzMCA4MEwxMTAgMTQwTDEzMCAyMDBMMTUwIDI0MEwxNzAgMjAwTDE5MCAxNDBMMTcwIDgwTDE1MCA0MFoiIGZpbGw9IiMyMjhCMjIiLz48cGF0aCBkPSJNMTUwIDQwTDE3MCAyNDBIMjAwTDE4MCAyMDBMMjAwIDEwMEwxNTAgNDBaIiBmaWxsPSIjMzNBQTMzIi8+PHBhdGggZD0iTTE1MCA0MEwxMzAgMjQwSDEwMEwxMjAgMjAwTDEwMCAxMDBMMTUwIDQwWiIgZmlsbD0iIzIyOEIyMiIvPjxjaXJjbGUgY3g9IjE0MCIgY3k9IjExMCIgcj0iNCIgZmlsbD0iI0ZGRkZGRiIvPjxjaXJjbGUgY3g9IjE2MCIgY3k9IjEzMCIgcj0iMyIgZmlsbD0iI0ZGRkZGRiIvPjwvc3ZnPg==',
            'banaba': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9IiNGOEZGRjgiLz48cGF0aCBkPSJNMTUwIDYwTDEyMCAxMjBMOTAgMTgwTDEyMCAyNDBIMTgwTDIxMCAxODBMMTgwIDEyMEwxNTAgNjBaIiBmaWxsPSIjMDA4QjAwIi8+PHBhdGggZD0iTTE1MCA2MEwxODAgMjQwSDIyMEwxOTAgMTgwTDIxMCAxMjBMMTUwIDYwWiIgZmlsbD0iIzAwQUEwMCIvPjxwYXRoIGQ9Ik0xNTAgNjBMMTIwIDI0MEg4MEwxMTAgMTgwTDkwIDEyMEwxNTAgNjBaIiBmaWxsPSIjMDA4QjAwIi8+PGNpcmNsZSBjeD0iMTQwIiBjeT0iMTMwIiByPSI1IiBmaWxsPSIjRkZGRkZGIi8+PGNpcmNsZSBjeD0iMTYwIiBjeT0iMTUwIiByPSI0IiBmaWxsPSIjRkZGRkZGIi8+PC9zdmc+'
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