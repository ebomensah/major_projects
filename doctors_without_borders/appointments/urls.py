from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, ConsultationViewSet, DoctorAvailabilityViewSet
from .views import AppointmentListView, ConsultationListView, BookAppointmentView, ConsultationCreateView
from .views import (
    AppointmentDetailView, AppointmentUpdateView, AppointmentDeleteView,
    ConsultationDetailView, ConsultationUpdateView, ConsultationDeleteView,
    PharmacistPrescriptionListView, MarkPrescriptionAsServedView,  DoctorAvailabilityListView,
    DoctorAvailabilityCreateView,DoctorAvailabilityDeleteView, DoctorAvailabilityUpdateView, get_prescriptions
)
from .views import AvailableDoctorsListView

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'consultations', ConsultationViewSet, basename='consultation')
router.register(r'availability', DoctorAvailabilityViewSet, basename='availability')

urlpatterns =[
    path('api/', include(router.urls)),
    
    path("appointments/book/", BookAppointmentView.as_view(), name='book-appointment'),
    path("appointments/", AppointmentListView.as_view(), name="appointments_list"),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),

    # Show all available slots (for patient to choose from)
    path('appointments/available-doctors/', AvailableDoctorsListView.as_view(), name='available-doctors'),

    # Consultations
    path("consultations/create/<int:appointment_id>/", ConsultationCreateView.as_view(), name='create-consultation'),
    path("consultations/", ConsultationListView.as_view(), name="consultations_list"),
    path('consultations/<int:pk>/', ConsultationDetailView.as_view(), name='consultation-detail'),
    path('consultations/<int:pk>/update/', ConsultationUpdateView.as_view(), name='consultation-update'),
    path('consultations/<int:pk>/delete/', ConsultationDeleteView.as_view(), name='consultation-delete'),
    path('pharmacist/prescriptions/', PharmacistPrescriptionListView.as_view(), name='pharmacist-prescriptions'),
    path('pharmacist/prescriptions/<int:pk>/serve/', MarkPrescriptionAsServedView.as_view(), name='mark-prescription-served'),
    path('api/pharmacist/prescriptions/', get_prescriptions, name='get_prescriptions'),

# Doctor Availability
    path('availability/', DoctorAvailabilityListView.as_view(), name='availability-list'),
    path('availability/create/', DoctorAvailabilityCreateView.as_view(), name='availability-create'),
    path('availability/<int:pk>/edit/', DoctorAvailabilityUpdateView.as_view(), name='availability-edit'),
    path('availability/<int:pk>/delete/', DoctorAvailabilityDeleteView.as_view(), name='availability-delete'),

# PatientBooking
    
]
