import json
from datetime import datetime, timedelta
import os

with open('games/ESPORTSTMNT03_3196037.json', 'r') as data_file:
    json_data = data_file.read()

events = json.loads(json_data)

def get_relevant_data(event):
    data = dict()

    data["eventTime"] = event["eventTime"]
    data["eventType"] = event["eventType"]
    event_type = event["eventType"]

    # get info based on event type
    if event_type == "game_info":
        pass

    return data

# Function to group events into 5-minute intervals
def group_events_by_interval(events):
    interval_length = 5  # in minutes
    grouped_events = []
    current_interval_start = None
    current_interval_events = []

    for event in events:
        event_time = datetime.fromisoformat(event["eventTime"][:-1])  # Parse event time
        if current_interval_start is None:
            current_interval_start = event_time

        # Check if event is within the current interval
        if event_time <= current_interval_start + timedelta(minutes=interval_length):
            current_interval_events.append(get_relevant_data(event))
        else:
            grouped_events.append(current_interval_events)
            current_interval_events = [get_relevant_data(event)]
            current_interval_start = event_time

    # Add the last interval
    grouped_events.append(current_interval_events)
    return grouped_events

# Group events into 5-minute intervals
grouped_events = group_events_by_interval(events)

if not os.path.exists('intervals/'):
    cwd = os.path.abspath(os.getcwd())
    os.makedirs(os.path.join(cwd, 'intervals/'))

with open('intervals/ESPORTSTMNT03_3196037.json', 'w') as data_file:
    json.dump(grouped_events, data_file, indent=4)
