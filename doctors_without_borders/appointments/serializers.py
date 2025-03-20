# Edited this to reflect slots for appointments. with start time endtime
from rest_framework import serializers
from .models import Appointment, Availability, Consultation
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import Availability

User = get_user_model()

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 'reason', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(role='doctor')

    def validate(self, data):
        doctor = data.get('doctor')
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # 1. End time must be after start time
        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        # 2. Match with an availability block
        try:
            availability = Availability.objects.get(
                doctor=doctor,
                date=date,
                start_time__lte=start_time,
                end_time__gte=end_time
            )
        except Availability.DoesNotExist:
            raise serializers.ValidationError("Appointment is outside the doctor's availability.")

        # 3. Check duration matches availability slot duration
        delta = datetime.combine(date, end_time) - datetime.combine(date, start_time)
        if delta.total_seconds() % (availability.slot_duration * 60) != 0:
            raise serializers.ValidationError(
                f"Appointment duration must be a multiple of {availability.slot_duration} minutes."
            )

        # 4. Prevent overlap with existing appointments
        conflict = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if conflict:
            raise serializers.ValidationError("This time slot is already booked.")

        return data



class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'date', 'start_time', 'end_time', 'slot_duration']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data


class ConsultationSerializer(serializers.ModelSerializer):
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.none())  # Default to no appointments
    doctor_name = serializers.CharField(source='appointment.doctor.username', read_only=True)
    patient_name = serializers.CharField(source='appointment.patient.username', read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'doctor_name', 'patient_name','appointment', 'history', 'examination_findings', 'investigations', 'treatment_plan', 'prescriptions', 'status', 'review_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter appointments based on the logged-in user
        user = self.context['request'].user
        self.fields['appointment'].queryset = Appointment.objects.filter(doctor=user)  # Only show appointments for the logged-in doctor

    def validate_appointment(self, value):
        # Ensure the selected appointment belongs to the logged-in doctor
        doctor = self.context['request'].user
        if value.doctor != doctor:
            raise serializers.ValidationError("You are not authorized to create a consultation for this appointment.")
        return value

    def create(self, validated_data):
        validated_data.pop('doctor', None)
            
        consultation = Consultation.objects.create(
            **validated_data
        )
        return consultation


    def to_representation(self, instance):
        """
        Optionally modify the way data is returned for a consultation
        (e.g., include appointment details if needed).
        """
        representation = super().to_representation(instance)
        # Include doctor and patient details in the representation
        representation['appointment'] = {
            'id': instance.appointment.id,
            'date_time': instance.appointment.date_time,
            'patient': instance.appointment.patient.username,
            'doctor': instance.appointment.doctor.username,
        }
        return representation