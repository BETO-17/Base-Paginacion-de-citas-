from django.db import models

class Appointment(models.Model):
    ghl_id = models.CharField(max_length=100, unique=True)  # ID que devuelve GHL
    calendar_id = models.CharField(max_length=100)
    contact_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or 'Sin título'} ({self.ghl_id})"

