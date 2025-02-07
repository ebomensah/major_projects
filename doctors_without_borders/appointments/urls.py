from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, ConsultationViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'consultations', ConsultationViewSet, basename='consultation')

urlpatterns =[
    path('', include(router.urls)),
]