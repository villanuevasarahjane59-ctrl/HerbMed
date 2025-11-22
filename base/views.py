from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import CustomUser, Herb
from .models import Herb
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponse
import json

def homepage(request):
    return render(request, "registration/homepage.html")

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Make first user admin
            User = get_user_model()
            if User.objects.count() == 1:
                user.is_staff = True
                user.is_superuser = True
                user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/registration.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Log In Successfully. Welcome to HERBMED!")

                if user.is_staff:
                    return redirect("adminpanel")
                return redirect("user_dashboard")

            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "registration/registration.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required
def user_dashboard(request):
    herbs = Herb.objects.all()

    conditions = {
        'cough': 'Cough Remedies',
        'cold': 'Cold & Flu Remedies',
        'fever': 'Fever Reducers',
        'skin': 'Skin Allergy Relief',
        'wound': 'Natural Wound Care',
    }

    grouped_herbs_display = {}
    
    seen = set()   # <--- track herb names already displayed

    for herb in herbs:

        # If we've already displayed an herb with the same name, skip it
        if herb.name.lower() in seen:
            continue

        # mark this herb name as shown
        seen.add(herb.name.lower())

        # normal grouping logic
        condition_key = herb.condition
        if condition_key not in grouped_herbs_display:
            grouped_herbs_display[condition_key] = {
                "display_name": conditions.get(condition_key, condition_key.title()),
                "herbs": []
            }
        
        grouped_herbs_display[condition_key]["herbs"].append(herb)

    return render(request, "registration/user_dashboard.html", {
        "grouped_herbs": grouped_herbs_display
    })

@login_required
def adminpanel(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admins only.")
        return redirect("user_dashboard")

    herbs = Herb.objects.all().order_by("-created_at")
    return render(request, "registration/adminpanel.html", {"herbs": herbs})

@login_required
def add_herb(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect("user_dashboard")

    if request.method == "POST":
        name = request.POST.get("name")
        scientific_name = request.POST.get('scientific_name')
        condition = request.POST.get("condition")
        benefits = request.POST.get("benefits")
        procedure = request.POST.get("procedure")
        prescription = request.POST.get("prescription")
        advice = request.POST.get("advice")
        image = request.FILES.get("image")

        # MULTIPLE LOCATIONS
        locations_json = request.POST.get("location_list")
        locations = json.loads(locations_json) if locations_json else []

        # Save herb
        herb = Herb.objects.create(
            name=name,
            scientific_name=scientific_name,
            condition=condition,
            benefits=benefits,
            procedure=procedure,
            prescription=prescription,
            advice=advice,
            image=image,
            locations=locations  # MUST USE JSONFIELD IN MODEL
        )

        messages.success(request, f"{name} has been added successfully!")
        return redirect("adminpanel")

    return render(request, "registration/add_herb.html")

@login_required
def edit_herb(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect("user_dashboard")

    herb = get_object_or_404(Herb, pk=pk)

    if request.method == "POST":
        # basic fields
        herb.name = request.POST.get("name", herb.name)
        herb.scientific_name = request.POST.get("scientific_name", herb.scientific_name)
        herb.condition = request.POST.get("condition", herb.condition)
        herb.benefits = request.POST.get("benefits", herb.benefits)
        herb.procedure = request.POST.get("procedure", herb.procedure)
        herb.prescription = request.POST.get("prescription", herb.prescription)
        herb.advice = request.POST.get("advice", herb.advice)

        # image (optional)
        if request.FILES.get("image"):
            herb.image = request.FILES["image"]

        # --- LOCATION HANDLING ---
        # 1) If a JSON 'location_list' was submitted (from the edit form), parse and save it:
        location_list_raw = request.POST.get("location_list")
        if location_list_raw:
            try:
                parsed = json.loads(location_list_raw)
                # Basic validation: ensure parsed is a list of objects with lat & lng
                cleaned = []
                for item in parsed:
                    if isinstance(item, dict) and "lat" in item and "lng" in item:
                        try:
                            lat = float(item["lat"])
                            lng = float(item["lng"])
                            cleaned.append({"lat": lat, "lng": lng})
                        except (TypeError, ValueError):
                            # skip invalid coordinate
                            continue
                # Save as herb.locations (JSONField)
                herb.locations = cleaned
            except json.JSONDecodeError:
                # ignore invalid JSON (optionally add a message)
                messages.warning(request, "Could not parse location data; locations unchanged.")
        else:
            # 2) Fallback: if individual latitude/longitude hidden fields are used, update single-location list
            lat_raw = request.POST.get("latitude")
            lng_raw = request.POST.get("longitude")
            if lat_raw and lng_raw:
                try:
                    lat = float(lat_raw)
                    lng = float(lng_raw)
                    herb.locations = [{"lat": lat, "lng": lng}]
                except (TypeError, ValueError):
                    # ignore invalid floats
                    pass

        # Save changes
        herb.save()
        messages.success(request, f"{herb.name} has been updated successfully!")
        return redirect("adminpanel")

    # --- Prepare extra attributes for the template (so template can use herb.latitude, herb.longitude, herb.locations_json) ---
    # Ensure herb.locations is always a list
    if not herb.locations:
        herb.locations = []

    # Temporary convenience attributes for template rendering (these are NOT model fields)
    try:
        herb.locations_json = json.dumps(herb.locations)
    except TypeError:
        # if some value is unserializable, fallback to empty list
        herb.locations_json = "[]"

    if len(herb.locations) > 0 and isinstance(herb.locations[0], dict):
        first = herb.locations[0]
        herb.latitude = first.get("lat") or ""
        herb.longitude = first.get("lng") or ""
    else:
        herb.latitude = ""
        herb.longitude = ""

    return render(request, "registration/edit_herb.html", {"herb": herb})


@login_required
def delete_herb(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect("user_dashboard")

    herb = get_object_or_404(Herb, pk=pk)

    if request.method == "POST":
        herb.delete()
        messages.success(request, f"{herb.name} has been deleted.")
        return redirect("adminpanel")

    return render(request, "registration/delete_herb.html", {"herb": herb})

User = get_user_model()

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        username = user.username  # store before deleting

        # Log out the user first
        logout(request)

        # Delete the account
        user.delete()

        messages.success(request, f"Account '{username}' has been deleted successfully.")
        return redirect('home')  # redirect to your homepage or login page
    
    # If GET request, show a confirmation page
    return render(request, 'accounts/delete_acc.html')

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
    
    return HttpResponse('Admin user created successfully! Username: admin, Password: herbmed123')

def populate_herbs(request):
    from django.core.management import call_command
    from io import StringIO
    
    out = StringIO()
    call_command('populate_herbs', stdout=out)
    output = out.getvalue()
    
    return HttpResponse(f'Herbs populated successfully!<br><pre>{output}</pre>')

def run_migrations(request):
    from django.core.management import call_command
    from io import StringIO
    
    out = StringIO()
    call_command('create_migration', stdout=out)
    output = out.getvalue()
    
    return HttpResponse(f'Migrations completed!<br><pre>{output}</pre>')
