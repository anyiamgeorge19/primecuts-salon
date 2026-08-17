from django.contrib import admin
from .models import Availability, Appointment


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("stylist", "weekday", "start_time", "end_time")
    list_filter = ("weekday", "stylist")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("client", "stylist", "service", "date", "start_time", "status")
    list_filter = ("status", "stylist", "date")
    search_fields = ("client__username", "stylist__username")
