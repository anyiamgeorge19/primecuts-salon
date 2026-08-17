from django.shortcuts import render
from django.contrib.auth import get_user_model

from services.models import Service

User = get_user_model()


def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    stylists = User.objects.filter(role="stylist")[:4]
    return render(request, "core/home.html", {"services": services, "stylists": stylists})


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")
