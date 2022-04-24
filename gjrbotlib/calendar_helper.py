import requests
import arrow
import icalendar
import recurring_ical_events


def get_sorted_events_next_4_weeks(calendar_url):
    c = icalendar.Calendar.from_ical(requests.get(calendar_url).text)
    
    now = arrow.utcnow()
    next_month = arrow.utcnow().shift(months=1)

    next_4_weeks = recurring_ical_events.of(c).between(now.datetime, next_month.datetime)
    next_4_weeks = sorted(next_4_weeks, key=lambda e: arrow.get(e['DTSTART'].dt))
    
    return next_4_weeks
