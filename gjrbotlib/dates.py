import requests
import arrow
from ics import Calendar


def get_dates_next_month(url, calendar_name):
    c = Calendar(requests.get(url).text)

    now = arrow.utcnow()
    next_month = arrow.utcnow().shift(months=1)

    next_4_weeks = [ event for event in c.events if event.begin.is_between(now, next_month) ]
    next_4_weeks.sort()

    lines = []
    lines.append("Termine für '{}' in den nächsten 4 Wochen:".format(calendar_name))
    lines.append("")

    for e in next_4_weeks:
        lines.append("{}: {}".format(e.begin.to('Europe/Berlin').format('DD.MM.YYYY, HH:mm'), e.name))

    text = "".join([ line + '\n' for line in lines])

    return text

def make_date_summary(gjr_calendar_url, gjr_vorstands_calendar_url = None):

    text = get_dates_next_month(gjr_calendar_url, "GJR Kalender")
    
    if gjr_vorstands_calendar_url is not None:
        text += '\n\n'
        text += get_dates_next_month(gjr_vorstands_calendar_url, "GJR Vorstands Kalender")
    
    return text
