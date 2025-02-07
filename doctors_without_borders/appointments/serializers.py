from rest_framework import serializers
from .models import Appointment, Consultation
from django.contrib.auth import get_user_model

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date_time', 'reason', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = get_user_model().objects.filter(role='doctor')


class ConsultationSerializer(serializers.ModelSerializer):
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.none())  # Default to no appointments

    class Meta:
        model = Consultation
        fields = ['appointment', 'history', 'examination_findings', 'investigations', 'treatment_plan', 'prescriptions', 'status', 'review_date']

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