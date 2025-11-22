from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin_user(request):
    User = get_user_model()
    
    # Delete existing admin if exists
    User.objects.filter(username='admin').delete()
    
    # Create new superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@herbmed.com',
        password='herbmed123',
        fullname='Admin User'
    )
    
    return HttpResponse(f'Admin user created successfully! Username: admin, Password: herbmed123')