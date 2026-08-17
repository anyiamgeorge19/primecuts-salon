from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for Prime Cuts Salon & Barbershop.
    A single table serves three roles: client, stylist, and admin/staff.
    """

    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        STYLIST = "stylist", "Stylist"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    phone_number = models.CharField(max_length=20, blank=True)

    # Extra fields that only apply to stylists -- harmless/blank for clients.
    bio = models.TextField(blank=True, help_text="Shown on the stylist's public profile.")
    specialization = models.CharField(max_length=150, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def is_stylist(self):
        return self.role == self.Role.STYLIST

    def is_client(self):
        return self.role == self.Role.CLIENT

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
