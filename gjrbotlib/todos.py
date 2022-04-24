import requests
import re

def parse_vosi_pad_for_todos(vosi_pad_url):
    """ Returns a string containing the TODOs """
    r = requests.get(vosi_pad_url, allow_redirects=True)
    content = r.content.decode('utf-8')

    matched_todos = {}
    unmatched_todos = []

    heading_count = 0
    heading = ""

    for line in content.splitlines():
        
        if len(line.strip()) > 0 and line.strip()[0] == '#':
            continue

        # Try to figure out in what meeting we are
        if line.count("Vorstandssitzung am"):
            heading_count += 1

            # Only break if we found at least one item
            if heading_count > 1 and (len(matched_todos) + len(unmatched_todos)) != 0:
                break

            heading = line.strip()

        # Extract the TODOs
        if line.count("TODO"):
            match = re.search(r"^.*TODO:(.*)(\(.*\))$", line)

            if match:
                task = match.group(1).strip()
                assignees = match.group(2)[1:-1].strip().lower().split(',')
                assignees = [ a.strip() for a in assignees ]
                
                for assignee in assignees:
                    if not assignee in matched_todos:
                        matched_todos[assignee] = []

                    matched_todos[assignee].append(task)
            else:
                pos = line.find("TODO")
                unmatched_todos.append(line[pos+4:])

    # Print the stuff
    lines = []
    lines.append("Tasks from '{}':".format(heading))
    lines.append("")

    for assignee in matched_todos.keys():
        lines.append(assignee.upper())
        for task in matched_todos[assignee]:
            lines.append("- {}".format(task))
        lines.append("")

    text = "".join([ line + '\n' for line in lines])

    return text



def parse_all_todos_of_person(person, vosi_pad_url):
    ''' returns a string containing the todos '''
    
    r = requests.get(vosi_pad_url, allow_redirects=True)
    content = r.content.decode('utf-8')
    
    todos = {}
    current_meeting = ""
    
    for line in content.splitlines():
        if len(line.strip()) > 0 and line.strip()[0] == '#':
            continue
                
        # Try to figure out in what meeting we are
        if line.count("Vorstandssitzung am"):
            current_meeting = line.strip()
            todos[current_meeting] = []
            
        if line.count("TODO"):
            match = re.search(r"^.*TODO:(.*)(\(.*\))$", line)

            if match:
                task = match.group(1).strip()
                assignees = match.group(2)[1:-1].strip().lower().split(',')
                assignees = [ a.strip() for a in assignees ]

                if person.lower() in assignees:
                    todos[current_meeting].append(task)
    
    lines = []
    lines.append("Tasks for '{}':".format(person.upper()))
    lines.append("")
    
    found_at_least_one = False
    
    for date in todos.keys():
        if len(todos[date]) == 0:
            continue
        else:
            found_at_least_one = True
        
        lines.append(date)
        for task in todos[date]:
            lines.append("- {}".format(task))
        lines.append("")
        
    if not found_at_least_one:
        return "Error: Did not find any TODOs for person '{}'".format(person)
            
    text = "".join([ line + '\n' for line in lines])
    return text
