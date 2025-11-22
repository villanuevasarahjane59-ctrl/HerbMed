from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- Public Homepage ---
    path('', views.homepage, name='homepage'),  # accessible to everyone

    # --- Auth routes ---
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),

    # --- User Dashboard (requires login) ---
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    # --- Admin Dashboard ---
    path('adminpanel/', views.adminpanel, name='adminpanel'),

    # --- Admin CRUD for Herbs ---
    path('adminpanel/add/', views.add_herb, name='add_herb'),
    path('adminpanel/edit/<int:pk>/', views.edit_herb, name='edit_herb'),
    path('adminpanel/delete/<int:pk>/', views.delete_herb, name='delete_herb'),

     path('delete-account/', views.delete_account, name='delete_account'),
     path('create-admin/', views.create_admin_user, name='create_admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    