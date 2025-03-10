from .models import Consultation, Appointment
from .permissions import DoctorsOnly
from .serializers import AppointmentSerializer, ConsultationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status 
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import AppointmentForm, ConsultationForm
from django.contrib import messages



def get_prescriptions(request):
    prescriptions = Consultation.objects.exclude(prescriptions="")

    # Create a list of prescriptions to send as JSON
    data = [
        {
            "patient": f"{c.appointment.patient.first_name} {c.appointment.patient.last_name}",
            "doctor": f"Dr. {c.appointment.doctor.first_name} {c.appointment.doctor.last_name}",
            "prescriptions": c.prescriptions
        }
        for c in prescriptions
    ]

    # Ensure that we are sending prescriptions as an empty list if none found
    if not data:
        data = []

    return JsonResponse({"prescriptions": data})

class PharmacistPrescriptionListView(LoginRequiredMixin, ListView):
    model= Consultation
    template_name= 'appointments/pharmacist_prescriptions.html'
    context_object_name = 'prescriptions'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'pharmacist':
            return Consultation.objects.filter(status="completed", prescriptions__isnull=False, prescriptions__gt="", prescription_served=False)
        return Consultation.objects.none()


class MarkPrescriptionAsServedView(UpdateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        if user.role != 'pharmacist':
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        try:
            consultation = Consultation.objects.get(id=kwargs['pk'])
            consultation.prescription_served = True
            consultation.save()
            return Response({"message": "Prescription marked as served."}, status=status.HTTP_200_OK)
        except Consultation.DoesNotExist:
            return Response({"error": "Consultation not found"}, status=status.HTTP_404_NOT_FOUND)



@method_decorator(login_required, name='dispatch')
class BookAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments_list')  # Redirect to the appointments list page after booking

    def form_valid(self, form):
        # Set the logged-in user as the patient of the appointment
        form.instance.patient = self.request.user
        return super().form_valid(form)

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'

class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'

    def test_func(self):
        """ Ensure only the assigned doctor can edit the appointment. """
        appointment = self.get_object()
        return self.request.user == appointment.doctor

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to edit this appointment.")
        return redirect('home')

class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name= 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)
    

class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointments-list')

    def test_func(self):
        appointment = self.get_object()
        return self.request.user == appointment.doctor

class ConsultationCreateView( LoginRequiredMixin, CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'appointments/consultation_create.html'

    def form_valid(self, form):
        appointment_id = self.kwargs['appointment_id']
        appointment = get_object_or_404(Appointment, id='appointment_id')
        form.instance.appointment=appointment
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the consultations list after creating the consultation
        return redirect('consultations_list')
    
class ConsultationDetailView(LoginRequiredMixin, DetailView):
    model = Consultation
    template_name = 'appointments/consultation_detail.html'
    context_object_name = 'consultation'

class ConsultationUpdateView(UpdateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'appointments/consultation_form.html'
    success_url = reverse_lazy('consultations_list')

    def test_func(self):
        consultation = self.get_object()
        return self.request.user == consultation.appointment.doctor

class ConsultationListView(LoginRequiredMixin, ListView):
    model = Consultation
    template_name = 'appointments/consultation_list.html'
    context_object_name = 'consultations'

    def get_queryset(self):
        if self.request.user.role == 'doctor':
            return Consultation.objects.filter(appointment__doctor=self.request.user)
        else:
            return Consultation.objects.none()
        
class ConsultationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Consultation
    template_name = 'appointments/consultation_confirm_delete.html'
    success_url = reverse_lazy('consultations-list')

    def test_func(self):
        consultation = self.get_object()
        return self.request.user == consultation.appointment.doctor

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


