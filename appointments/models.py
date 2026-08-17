from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from services.models import Service


class Availability(models.Model):
    """A recurring weekly time-window during which a stylist can be booked.
    e.g. Jide is available Mondays 09:00-13:00."""

    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    stylist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "stylist"},
        related_name="availabilities",
    )
    weekday = models.IntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["weekday", "start_time"]
        verbose_name_plural = "Availabilities"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

    def __str__(self):
        return f"{self.stylist} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"


class Appointment(models.Model):
    """A booking of one Service, with one stylist, by one client, at a specific date/time."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        limit_choices_to={"role": "client"}, related_name="appointments_as_client",
    )
    stylist = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        limit_choices_to={"role": "stylist"}, related_name="appointments_as_stylist",
    )
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments")

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True, help_text="Anything the client wants the stylist to know beforehand.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["stylist", "date", "start_time"],
                name="unique_stylist_slot",
            )
        ]

    def __str__(self):
        return f"{self.client} with {self.stylist} on {self.date} {self.start_time} ({self.status})"
