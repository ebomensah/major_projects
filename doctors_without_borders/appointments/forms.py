from django import forms    
from .models import Appointment, Consultation
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