from django.core.management.base import BaseCommand
from base.models import Herb

class Command(BaseCommand):
    help = 'Fix herb images to use hardcoded static paths'

    def handle(self, *args, **options):
        herbs = Herb.objects.all()
        updated_count = 0
        
        for herb in herbs:
            # Clear any uploaded images or URLs to force static mapping
            if herb.image or herb.image_url:
                herb.image = None
                herb.image_url = ''
                herb.save()
                updated_count += 1
                self.stdout.write(f"Updated {herb.name} to use static image")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} herbs to use hardcoded images')
        )