from django.urls import path
from .views import AvailabilityCalendarView, CalendarBookingView

urlpatterns = [
    path("calendar/", AvailabilityCalendarView.as_view(), name="calendar-view"),
    path("calendar/book/", CalendarBookingView.as_view(), name="calendar-book"),
]
