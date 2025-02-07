from django.contrib import admin
from .models import Appointment, Consultation
from users.models import Profile
from django.contrib.auth import get_user_model

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date_time', 'status', 'reason']
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = get_user_model().objects.filter(role="doctor")  # Ensure only doctors appear
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'date', 'history', 'examination_findings', 'treatment_plan', 'prescriptions', 'status', 'review_date']

    def doctor(self, obj):
        return obj.appointment.doctor
    
    def patient(self, obj):
        return obj.appointment.patient 
    

# Register your models here.
