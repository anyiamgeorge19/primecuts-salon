from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ClientSignUpForm, StylistProfileForm


def register(request):
    if request.method == "POST":
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Prime Cuts Salon & Barbershop! Your account has been created.")
            return redirect("core:home")
    else:
        form = ClientSignUpForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    if request.user.is_stylist():
        if request.method == "POST":
            form = StylistProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated.")
                return redirect("accounts:profile")
        else:
            form = StylistProfileForm(instance=request.user)
        return render(request, "accounts/profile_stylist.html", {"form": form})

    return render(request, "accounts/profile_client.html")
