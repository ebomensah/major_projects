from django import forms   
from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError 
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
            'date': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),  # HTML-level restriction
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'slot_duration': forms.NumberInput(attrs={'min': 15, 'step': 15}),
        }

    def clean_date(self):
        chosen_date = self.cleaned_data['date']
        if chosen_date < date.today():
            raise forms.ValidationError("You can't choose a past date.")
        return chosen_date
    
    def clean(self):
        cleaned_data = super().clean()
        date_selected = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        slot_duration = cleaned_data.get('slot_duration')

        if date_selected == date.today() and start_time:
            now_plus_one = (datetime.now() + timedelta(hours=1)).time()
            if start_time <= now_plus_one:
                self.add_error('start_time', "Start time must be at least one hour from now.")

        if start_time and end_time and start_time >= end_time:
            self.add_error('end_time', "End time must be after start time.")

        if start_time and end_time and slot_duration:
            total_minutes = (datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)).total_seconds() / 60
            if slot_duration > total_minutes:
                self.add_error('slot_duration', f"Slot duration ({slot_duration} mins) cannot be longer than the total available time ({int(total_minutes)} mins).")

  

        
