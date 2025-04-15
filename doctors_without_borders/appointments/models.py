from django.db import models
from django.contrib.auth import get_user_model
from users.models import CustomUser 
from datetime import date, datetime, timedelta


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'appointments_as_patient')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name= 'appointments_as_doctor')
    date_time = models.DateTimeField(unique= True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default = 'scheduled')
    reason = models.TextField(blank= True, null=True)
    notes = models.TextField(blank=True, null=True)
    availability = models.ForeignKey('Availability', on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient.title} {self.patient.first_name} {self.patient.last_name}'s Appointment with Dr. {self.doctor.first_name} {self.doctor.last_name} on {self.date_time}"

    class Meta:
        ordering = ['date_time'] 



class Availability(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.PositiveIntegerField(default=60, help_text="Slot duration in minutes")

    class Meta:
        unique_together = ('doctor', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor.get_full_name()} available on {self.date} from {self.start_time} to {self.end_time}"

    @property
    def total_slots(self):
        total_minutes = (datetime.combine(self.date, self.end_time) - datetime.combine(self.date, self.start_time)).total_seconds() / 60
        return int(total_minutes // self.slot_duration)

    @property
    def booked_slots(self):
        return self.appointments.count()

    @property
    def available_slots(self):
        return max(0, self.total_slots - self.booked_slots)

    def calculate_total_hours(self):
        delta = datetime.combine(self.date, self.end_time) - datetime.combine(self.date, self.start_time)
        return delta.total_seconds() / 3600

    def calculate_slot_count(self):
        return self.total_slots



class Consultation (models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('awaiting_review', 'Awaiting review'),
    ]
    date = models.DateTimeField(auto_now_add=True)
    history = models.TextField(blank=False)
    examination_findings = models.TextField(blank=True)
    investigations = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=False)
    prescriptions = models.TextField(blank=True)
    prescription_served = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='awaiting_review')
    review_date = models.DateField(blank=True, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name= 'consultation')

    def __str__(self):
        return f"Consultation for {self.appointment.patient} on {self.date}"