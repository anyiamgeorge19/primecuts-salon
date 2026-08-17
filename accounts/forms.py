from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class ClientSignUpForm(UserCreationForm):
    """Public registration form -- always creates a Client account.
    Stylist and Admin accounts are created by staff through the Django admin,
    which keeps the public site from letting anyone register as a stylist."""

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        if commit:
            user.save()
        return user


class StylistProfileForm(forms.ModelForm):
    """Lets a logged-in stylist edit their own public profile."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "bio", "specialization",
                  "years_of_experience", "profile_photo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "profile_photo":
                field.widget.attrs["class"] = "form-control"
