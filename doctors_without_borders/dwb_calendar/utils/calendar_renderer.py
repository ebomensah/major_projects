from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from appointments.models import Availability  # or wherever your Availability model is
import datetime

class AvailabilityCalendar(HTMLCalendar):
    def __init__(self, availabilities):
        super().__init__()
        self.availabilities = availabilities

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        day_avail = self.availabilities.filter(date__day=day)
        slots_html = ""
        for slot in day_avail:
            slots_html += f'<li>Dr. {slot.doctor.first_name} ({slot.start_time} - {slot.end_time})</li>'

        return f'<td class="{self.cssclasses[weekday]}"><span class="date">{day}</span><ul>{slots_html}</ul></td>'

    def formatweek(self, theweek):
        return '<tr>' + ''.join(self.formatday(d, wd) for (d, wd) in theweek) + '</tr>'

    def formatmonth(self, year, month, withyear=True):
        availabilities = self.availabilities.filter(date__year=year, date__month=month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(year, month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(year, month):
            cal += f'{self.formatweek(week)}\n'
        cal += '</table>'

        return mark_safe(cal)
