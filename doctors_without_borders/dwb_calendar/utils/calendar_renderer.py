from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from appointments.models import Availability  # or wherever your Availability model is
import datetime
from django.utils.safestring import mark_safe

class AvailabilityCalendar(HTMLCalendar):
    def __init__(self, availabilities):
        super().__init__()
        self.availabilities = availabilities

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday" style="border: 1px solid #ccc;">&nbsp;</td>'

        slots_html = "<ul style='padding-left: 1em; font-size: 0.8rem;'>"
        for slot in self.current_month_availabilities.filter(date__day=day):
            slots_html += f"""
                <li style='margin-bottom: 4px;'>
                    <button style='font-size: 0.7rem;' onclick="openModal('{slot.id}', '{slot.doctor.first_name}', '{slot.date}', '{slot.start_time}', '{slot.end_time}')">
                        Dr. {slot.doctor.first_name} ({slot.start_time} - {slot.end_time})
                    </button>
                </li>
            """
        slots_html += "</ul>"

        return f'<td class="{self.cssclasses[weekday]}" style="height: 160px; vertical-align: top; border: 1px solid #ccc; padding: 6px;">' + \
            f'<span class="date" style="font-weight: bold;">{day}</span>{slots_html}</td>'


    def formatweek(self, theweek):
        return '<tr>' + ''.join(self.formatday(d, wd) for (d, wd) in theweek) + '</tr>'

    def formatmonth(self, year, month, withyear=True):
        self.current_month_availabilities = self.availabilities.filter(date__year=year, date__month=month)

        cal = '<table class="calendar" style="width: 100%; table-layout: fixed; border-collapse: collapse;">\n'
        cal += self.formatmonthname(year, month, withyear=withyear) + '\n'
        cal += self.formatweekheader() + '\n'
        for week in self.monthdays2calendar(year, month):
            cal += self.formatweek(week) + '\n'
        cal += '</table>'

        return mark_safe(cal)
