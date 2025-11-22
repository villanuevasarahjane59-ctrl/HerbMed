import os
import shutil
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class StaticFileStorage(FileSystemStorage):
    """Custom storage that saves uploaded files to static directory"""
    
    def __init__(self):
        # Save to static directory instead of media
        static_herbs_path = os.path.join(settings.BASE_DIR, 'base', 'static', 'base', 'uploaded_herbs')
        os.makedirs(static_herbs_path, exist_ok=True)
        super().__init__(location=static_herbs_path, base_url='/static/base/uploaded_herbs/')
    
    def _save(self, name, content):
        # Save the file and return the path
        saved_name = super()._save(name, content)
        return saved_name
    
    def url(self, name):
        # Return static URL instead of media URL
        return f'/static/base/uploaded_herbs/{name}'