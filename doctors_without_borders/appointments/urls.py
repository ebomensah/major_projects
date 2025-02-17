from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, ConsultationViewSet
from .views import AppointmentListView, ConsultationListView, BookAppointmentView, ConsultationCreateView
from .views import (
    AppointmentDetailView, AppointmentUpdateView, AppointmentDeleteView,
    ConsultationDetailView, ConsultationUpdateView, ConsultationDeleteView
)


router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'consultations', ConsultationViewSet, basename='consultation')

urlpatterns =[
    path('api/', include(router.urls)),
    path("appointments/book/", BookAppointmentView.as_view(), name='book-appointment'),
    path("appointments/", AppointmentListView.as_view(), name="appointments_list"),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path("consultations/create/<int:appointment_id>/", ConsultationCreateView.as_view(), name='create-consultation'),
    path("consultations/", ConsultationListView.as_view(), name="consultations_list"),
    path('consultations/<int:pk>/', ConsultationDetailView.as_view(), name='consultation-detail'),
    path('consultations/<int:pk>/update/', ConsultationUpdateView.as_view(), name='consultation-update'),
    path('consultations/<int:pk>/delete/', ConsultationDeleteView.as_view(), name='consultation-delete'),
]
