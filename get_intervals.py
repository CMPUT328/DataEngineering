import json
from datetime import datetime, timedelta
import os



def get_relevant_data(event):
    data = dict()

    if event["eventType"] == "building_destroyed":
        data["teamID"] = event["teamID"]
    
    if event["eventType"] == "champion_kill":
        data['victimTeamID'] = event['victimTeamID']
        data['victim'] = event['victim']
        data['killerTeamID'] = event['killerTeamID']

    if event["eventType"] == "epic_monster_kill":
        data['killerTeamID'] = event['killerTeamID']
        data['killer'] = event['killer']
        data['monsterType'] = event['monsterType']

    if event["eventType"] == "turret_plate_destroyed":
        data['teamID'] = event['teamID']

    if event["eventType"] == "game_end":
        data['winningTeam'] = event['winningTeam']
        
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

def get_events_from_file(file_name, path):
    path = os.path.join(path, file_name)
    with open(path, "r") as json_file:
        json_data = json_file.read()
    events = json.loads(json_data)
    grouped_events = group_events_by_interval(events)

    output_path = os.path.join(os.path.abspath(os.getcwd()), 'DataEngineering/games/intervals/')
    if not os.path.exists(output_path):
        cwd = os.path.abspath(os.getcwd())
        os.makedirs(output_path)

    output_file = output_path + "/" + file_name
    print(output_file)
    with open(output_file, 'w') as data_file:
        json.dump(grouped_events, data_file, indent=4)

cwd = os.path.abspath(os.getcwd())
path = os.path.join(cwd, 'DataEngineering/games/')
for file in os.listdir(path):
    get_events_from_file(file, path)
