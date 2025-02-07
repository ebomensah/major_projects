from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment, Consultation
from notifications.models import Notification

# Notify doctor when a new appointment is created
@receiver(post_save, sender=Appointment)
def notify_doctor_on_appointment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.doctor,
            message=f"You have a new appointment with {instance.patient.username} on {instance.date_time}."
        )

# Notify patient when a consultation is created
@receiver(post_save, sender=Consultation)
def notify_patient_on_consultation(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.appointment.patient,
            message=f"Your consultation from {instance.date} has been added by Dr. {instance.appointment.doctor.username}."
        )