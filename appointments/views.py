import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from services.models import Service
from .models import Appointment, Availability
from .forms import AppointmentForm

User = get_user_model()


def stylist_list(request):
    stylists = User.objects.filter(role="stylist")
    return render(request, "appointments/stylist_list.html", {"stylists": stylists})


def stylist_detail(request, pk):
    stylist = get_object_or_404(User, pk=pk, role="stylist")
    availabilities = stylist.availabilities.all()
    return render(
        request, "appointments/stylist_detail.html",
        {"stylist": stylist, "availabilities": availabilities},
    )


def available_slots(request):
    """AJAX-style helper: given stylist, service and date, return free start times.
    Used by the booking page to populate a dropdown of real, bookable slots."""
    stylist_id = request.GET.get("stylist")
    service_id = request.GET.get("service")
    date_str = request.GET.get("date")

    try:
        stylist = User.objects.get(pk=stylist_id, role="stylist")
        service = Service.objects.get(pk=service_id)
        date = datetime.date.fromisoformat(date_str)
    except (User.DoesNotExist, Service.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"slots": []})

    windows = Availability.objects.filter(stylist=stylist, weekday=date.weekday())
    duration = datetime.timedelta(minutes=service.duration_minutes)
    booked = set(
        Appointment.objects.filter(stylist=stylist, date=date)
        .exclude(status=Appointment.Status.CANCELLED)
        .values_list("start_time", flat=True)
    )

    slots = []
    for window in windows:
        current = datetime.datetime.combine(date, window.start_time)
        end_of_window = datetime.datetime.combine(date, window.end_time)
        while current + duration <= end_of_window:
            slot_time = current.time()
            if slot_time not in booked:
                slots.append(slot_time.strftime("%H:%M"))
            current += duration

    return JsonResponse({"slots": slots})


@login_required
def book_appointment(request):
    if not request.user.is_client():
        messages.error(request, "Only client accounts can book appointments.")
        return redirect("core:home")

    preselected_stylist = request.GET.get("stylist")
    preselected_service = request.GET.get("service")

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.status = Appointment.Status.PENDING
            appointment.save()
            messages.success(
                request,
                "Your appointment request has been sent. You'll be notified once the stylist confirms it.",
            )
            return redirect("appointments:my_appointments")
    else:
        initial = {}
        if preselected_stylist:
            initial["stylist"] = preselected_stylist
        if preselected_service:
            initial["service"] = preselected_service
        form = AppointmentForm(initial=initial)

    services = Service.objects.filter(is_active=True)
    stylists = User.objects.filter(role="stylist")
    return render(
        request, "appointments/book_appointment.html",
        {"form": form, "services": services, "stylists": stylists},
    )


@login_required
def my_appointments(request):
    if not request.user.is_client():
        return redirect("appointments:stylist_dashboard")
    appointments = request.user.appointments_as_client.all()
    return render(request, "appointments/my_appointments.html", {"appointments": appointments})


@login_required
@require_POST
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    is_owner = appointment.client_id == request.user.id or appointment.stylist_id == request.user.id
    if not is_owner:
        messages.error(request, "You cannot cancel this appointment.")
    else:
        appointment.status = Appointment.Status.CANCELLED
        appointment.save()
        messages.success(request, "Appointment cancelled.")
    if request.user.is_stylist():
        return redirect("appointments:stylist_dashboard")
    return redirect("appointments:my_appointments")


@login_required
def stylist_dashboard(request):
    if not request.user.is_stylist():
        return redirect("appointments:my_appointments")
    appointments = request.user.appointments_as_stylist.all()
    return render(request, "appointments/stylist_dashboard.html", {"appointments": appointments})


@login_required
@require_POST
def update_status(request, pk, new_status):
    appointment = get_object_or_404(Appointment, pk=pk, stylist=request.user)
    valid_statuses = dict(Appointment.Status.choices)
    if new_status in valid_statuses:
        appointment.status = new_status
        appointment.save()
        messages.success(request, f"Appointment marked as {valid_statuses[new_status]}.")
    return redirect("appointments:stylist_dashboard")
