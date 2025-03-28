from django import forms

class CalendarBookingForm(forms.Form):
    time_slot = forms.ChoiceField(
        label="Select Time Slot",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        required=True
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        availability = kwargs.pop("availability", None)
        super().__init__(*args, **kwargs)

        if availability:
            # Dynamically generate time slots (every 30 mins)
            from datetime import datetime, timedelta, datetime as dt

            slots = []
            start = dt.combine(availability.date, availability.start_time)
            end = dt.combine(availability.date, availability.end_time)
            step = timedelta(minutes=availability.slot_duration)


            while start + step <= end:
                slot_label = start.strftime("%I:%M %p") + " - " + (start + step).strftime("%I:%M %p")
                slot_value = start.strftime("%Y-%m-%d %H:%M")
                slots.append((slot_value, slot_label))
                start += step

            self.fields["time_slot"].choices = slots
