from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment, Consultation
from .models import Notification

@receiver(post_save, sender=Appointment)
def notify_appointment_created(sender, instance, created, **kwargs):
    """Trigger notification when a new appointment is created."""
    if created:
        Notification.objects.create(
            recipient=instance.doctor,
            message=f"New appointment scheduled with {instance.patient.title} {instance.patient.first_name}{instance.patient.last_name} on {instance.date_time}."
        )

@receiver(post_save, sender=Consultation)
def notify_consultation_created(sender, instance, created, **kwargs):
    """Trigger notification when a new consultation is added."""
    if created:
        Notification.objects.create(
            recipient=instance.appointment.patient,
            message=f"Your consultation with Dr. {instance.appointment.doctor.first_name} {instance.appointment.doctor.last_name} has been recorded."
        )