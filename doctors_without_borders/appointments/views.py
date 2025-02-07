from .models import Consultation, Appointment
from .permissions import DoctorsOnly
from django.urls import reverse_lazy
from .serializers import AppointmentSerializer, ConsultationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status 
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.response import Response


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Ensure only the patient can view or delete their own appointments."""
        return Appointment.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


    def perform_destroy(self, instance):
        if instance.patient != self.request.user:
            raise PermissionDenied("You can only delete your own appointments.")
        instance.delete()


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [ DoctorsOnly, IsAuthenticated]

    def get_queryset(self):
        doctor = self.request.user
        return Consultation.objects.filter(appointment__doctor = doctor) 
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

    def perform_destroy(self, instance):
        if instance.doctor != self.request.user:
            raise PermissionDenied("Only the assigned doctor can delete this consultation.")
        instance.delete()


