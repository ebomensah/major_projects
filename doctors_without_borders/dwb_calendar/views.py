from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from appointments.models import Appointment, Availability
from .forms import CalendarBookingForm
from django.contrib import messages

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
