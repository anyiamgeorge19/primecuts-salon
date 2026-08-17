import datetime
from django import forms
from django.contrib.auth import get_user_model

from .models import Appointment, Availability

User = get_user_model()


class AppointmentForm(forms.ModelForm):
    """Client-facing booking form.
    The view narrows `stylist` and `date`/`start_time` choices to real
    availability before this form is shown; clean() re-checks on submit
    to guard against double-booking (race condition safety)."""

    class Meta:
        model = Appointment
        fields = ["service", "stylist", "date", "start_time", "notes"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-select"}),
            "stylist": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stylist"].queryset = User.objects.filter(role="stylist")

    def clean(self):
        cleaned = super().clean()
        stylist = cleaned.get("stylist")
        service = cleaned.get("service")
        date = cleaned.get("date")
        start_time = cleaned.get("start_time")

        if not (stylist and service and date and start_time):
            return cleaned

        if date < datetime.date.today():
            raise forms.ValidationError("You cannot book an appointment in the past.")

        # 1. Stylist must actually work that weekday, and slot must fit their window.
        end_time = (
            datetime.datetime.combine(date, start_time)
            + datetime.timedelta(minutes=service.duration_minutes)
        ).time()
        available = Availability.objects.filter(
            stylist=stylist, weekday=date.weekday(),
            start_time__lte=start_time, end_time__gte=end_time,
        )
        if not available.exists():
            raise forms.ValidationError(
                "This stylist is not available at that day/time. Please pick another slot."
            )

        # 2. Slot must not already be booked (pending or confirmed).
        clash = Appointment.objects.filter(
            stylist=stylist, date=date, start_time=start_time,
        ).exclude(status=Appointment.Status.CANCELLED)
        if self.instance.pk:
            clash = clash.exclude(pk=self.instance.pk)
        if clash.exists():
            raise forms.ValidationError("That slot was just booked by someone else. Please choose another time.")

        cleaned["end_time"] = end_time
        return cleaned

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.end_time = self.cleaned_data["end_time"]
        if commit:
            appointment.save()
        return appointment
