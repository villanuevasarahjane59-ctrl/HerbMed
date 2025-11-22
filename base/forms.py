from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

# ==========================
# LOGIN FORM
# ==========================
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Enter username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )


# ==========================
# USER / ADMIN REGISTRATION FORM
# ==========================
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}),
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email', 'username', 'password']
        widgets = {
            "fullname": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
        }

    # Validate that password and confirm_password match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    # Save method with optional admin privileges
    def save(self, commit=True, is_staff=False, is_superuser=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # hash password
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        if commit:
            user.save()
        return user
