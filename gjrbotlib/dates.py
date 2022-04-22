import requests
import arrow
import icalendar
import recurring_ical_events


def get_dates_next_month(url, calendar_name):
    c = icalendar.Calendar.from_ical(requests.get(url).text)

    now = arrow.utcnow()
    next_month = arrow.utcnow().shift(months=1)

    next_4_weeks = recurring_ical_events.of(c).between(now.datetime, next_month.datetime)
    next_4_weeks = sorted(next_4_weeks, key=lambda e: arrow.get(e['DTSTART'].dt))

    lines = []
    lines.append("Termine für '{}' in den nächsten 4 Wochen:".format(calendar_name))
    lines.append("")

    for e in next_4_weeks:
        name = e["SUMMARY"]
        begin = arrow.get(e['DTSTART'].dt)
        lines.append("{}: {}".format(begin.to('Europe/Berlin').format('DD.MM.YYYY, HH:mm'), name))

    text = "".join([ line + '\n' for line in lines])

    return text

def make_date_summary(gjr_calendar_url, gjr_vorstands_calendar_url = None):

    text = get_dates_next_month(gjr_calendar_url, "GJR Kalender")
    
    if gjr_vorstands_calendar_url is not None:
        text += '\n\n'
        text += get_dates_next_month(gjr_vorstands_calendar_url, "GJR Vorstands Kalender")
    
    return text
