from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from appointments.models import Appointment, Availability
from .forms import CalendarBookingForm
from django.contrib import messages
from django.views.generic import TemplateView
from datetime import date
from .utils.calendar_renderer import AvailabilityCalendar

class AvailabilityCalendarView(TemplateView):
    template_name = "calendar/calendar_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        year = self.request.GET.get("year", today.year)
        month = self.request.GET.get("month", today.month)

        availabilities = Availability.objects.all()
        calendar = AvailabilityCalendar(availabilities).formatmonth(int(year), int(month))

        context["calendar"] = calendar
        context["year"] = year
        context["month"] = month

        return context


class CalendarBookingView(View):
    def get(self, request):
        availability_id = request.GET.get("availability")
        availability = get_object_or_404(Availability, id=availability_id)

        form = CalendarBookingForm(availability=availability)
        context = {
            "form": form,
            "availability": availability
        }
        return render(request, "calendar/calendar_booking_form.html", context)

    def post(self, request):
        availability_id = request.GET.get("availability")
        availability = get_object_or_404(Availability, id=availability_id)

        form = CalendarBookingForm(request.POST, availability=availability)

        if form.is_valid():
            Appointment.objects.create(
                patient=request.user,
                doctor=availability.doctor,
                date_time=form.cleaned_data["time_slot"],
                reason=form.cleaned_data["reason"],
                notes=form.cleaned_data["notes"]
            )
            messages.success(request, "Appointment successfully booked.")
            return redirect("appointments_list")

        context = {
            "form": form,
            "availability": availability
        }
        return render(request, "calendar/calendar_booking_form.html", context)
