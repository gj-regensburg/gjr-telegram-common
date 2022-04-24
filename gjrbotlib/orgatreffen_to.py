import arrow
import re
import requests

from calendar_helper import get_sorted_events_next_4_weeks


def get_next_orgatreffen_to(url, make_url_from_date):
    try:
        next_4_weeks = get_sorted_events_next_4_weeks(url)
    except:
        return "Fehler beim Zugriff auf Kalender"
    
    next_orgatreffen = None
        
    for e in next_4_weeks:
        if "orgatreffen" in e["SUMMARY"].lower():
            next_orgatreffen = e
            break
    
    orgatreffen_begin = arrow.get(next_orgatreffen['DTSTART'].dt)
    pretty_date = orgatreffen_begin.to('Europe/Berlin').format('DD.MM.YYYY')
        
    if next_orgatreffen is None:
        return "Kein Orgatreffen in den nächsten 4 Wochen gefunden."
    
    url = make_url_from_date(orgatreffen_begin)
    
    try:
        r = requests.get(url, allow_redirects=True)
        content = r.content.decode('utf-8')
    except:
        return "Fehler beim Zugriff auf die Tagesordnung des Orgatreffens vom {}.".format(pretty_date)
    
    
    tops = []
    
    for line in content.splitlines():
        if len(line.strip()) > 0 and line.strip()[0] == '#':
            continue
        
        match = re.match("^(TOP (\d+|X)):\s*(.+)$", line)
        
        if match:
            tops.append(line.strip())
            
    if len(tops) == 0:
        return "Orgatreffen am {} gefunden, aber anscheinend gibt es noch keine Tagesordnung.".format(pretty_date)
            
    lines = []
    lines.append("Das nächste Orgatreffen findet am {} statt. Die Tagesordnung ist:".format(pretty_date))
    lines.append("")
    
    for top in tops:
        lines.append(top)
        
    return "".join([ line + '\n' for line in lines])
