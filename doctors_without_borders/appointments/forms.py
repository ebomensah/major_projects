from django import forms    
from .models import Appointment, Consultation, Availability

from django.contrib.auth import get_user_model

class AppointmentForm (forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason', 'notes']

    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs ={
            'type': 'datetime-local',
            'class': 'form-control',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = get_user_model().objects.filter(role='doctor')

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['history', 'examination_findings', 'treatment_plan', 'prescriptions', 'status', 'review_date']

    review_date = forms.DateTimeField(
        widget = forms.DateTimeInput(attrs={
            'type': 'datetime-local', 
            'class': 'form-control'}
        )
    )

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time', 'slot_duration']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'slot_duration': forms.NumberInput(attrs={'min': 15, 'step': 15}),
        }