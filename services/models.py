from django.db import models


class Service(models.Model):
    """A type of salon/barbershop service the business offers,
    e.g. Haircut, Beard Trim, Hair Coloring, Braiding."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(default=60)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True, help_text="Untick to hide from the public site without deleting it.")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
