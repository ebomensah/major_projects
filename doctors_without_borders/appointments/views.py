from .models import Consultation, Appointment, Availability
from .permissions import DoctorsOnly
from .serializers import AppointmentSerializer, ConsultationSerializer, AvailabilitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, generics 
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
from .forms import AppointmentForm, ConsultationForm, AvailabilityForm
from django.contrib import messages

from .models import Availability
from .serializers import AvailabilitySerializer
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Availability
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def get_prescriptions(request):
    prescriptions = Consultation.objects.filter(
        status="completed",
        prescriptions__isnull=False,
        prescriptions__gt="",
        prescription_served=False  # Ensure only unserved prescriptions are fetched
    )

    data = [
        {
            "id": c.id,  # Include prescription ID for the button
            "patient": f"{c.appointment.patient.first_name} {c.appointment.patient.last_name}",
            "doctor": f"Dr. {c.appointment.doctor.first_name} {c.appointment.doctor.last_name}",
            "prescriptions": c.prescriptions,
        }
        for c in prescriptions
    ]

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

    def post(self, request, *args, **kwargs):  # Change to POST
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

    def get_initial(self):
        initial = super().get_initial()
        doctor_id = self.request.GET.get('doctor')
        date_time = self.request.GET.get('date_time')

        if doctor_id:
            initial['doctor'] = doctor_id
        if date_time:
            initial['date_time'] = date_time

        return initial


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



# AVAILABILITY VIEW


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated, DoctorsOnly]

    def get_queryset(self):
        # Only return availability blocks for the logged-in doctor
        return Availability.objects.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class DoctorAvailabilityListView(LoginRequiredMixin, ListView):
    model = Availability
    template_name = 'availability/availability_list.html'
    context_object_name = 'availabilities'

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user)


class DoctorAvailabilityCreateView(LoginRequiredMixin, CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'availability/availability_form.html'
    success_url = reverse_lazy('availability-list')

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Only add total_hours and slot_count if the object exists (i.e., on edit, or if form is bound)
        form = context.get('form')
        if form and form.is_bound and form.is_valid():
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            slot_duration = form.cleaned_data.get('slot_duration')
            if start_time and end_time and slot_duration:
                from datetime import datetime, date
                total_minutes = (datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)).total_seconds() / 60
                context['total_hours'] = total_minutes / 60
                context['slot_count'] = int(total_minutes // slot_duration)
        return context



class DoctorAvailabilityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'availability/availability_form.html'
    success_url = reverse_lazy('availability-list')

    def test_func(self):
        availability = self.get_object()
        return self.request.user == availability.doctor
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        availability = self.object

        context['total_hours'] = availability.calculate_total_hours()
        context['slot_count'] = availability.calculate_slot_count()
        return context


class DoctorAvailabilityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Availability
    template_name = 'availability/availability_confirm_delete.html'
    success_url = reverse_lazy('availability-list')

    def test_func(self):
        availability = self.get_object()
        return self.request.user == availability.doctor


# PATIENTS AVAILABILTIY VIEW
class AvailableDoctorsListView(LoginRequiredMixin, ListView):
    model = Availability
    template_name = 'appointments/available_doctors.html'
    context_object_name = 'availabilities'

    def get_queryset(self):
        return Availability.objects.all().order_by('date')
