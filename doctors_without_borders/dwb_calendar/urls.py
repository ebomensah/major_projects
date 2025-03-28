from django.urls import path
from .views import AvailabilityCalendarView

urlpatterns = [
    path("calendar/", AvailabilityCalendarView.as_view(), name="calendar-view"),
]
