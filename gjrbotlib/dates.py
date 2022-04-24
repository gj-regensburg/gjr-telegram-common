import requests
import arrow
import icalendar
import recurring_ical_events

from gjrbotlib.calendar_helper import get_sorted_events_next_4_weeks


def get_dates_next_month(url, calendar_name):
    try:
        next_4_weeks = get_sorted_events_next_4_weeks(url)
    except:
        return "Fehler beim Zugriff auf Kalender"

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
