import json
from datetime import datetime, timedelta
import os
import sqlite3

def get_participants_and_teams(platform_game_id):
    conn = sqlite3.connect('mapping_data.db')
    cursor = conn.cursor()

    # Retrieve participant IDs and team IDs for the given platform_game_id
    cursor.execute('''
        SELECT participant_1, participant_2, participant_3, participant_4, participant_5,
               participant_6, participant_7, participant_8, participant_9, participant_10,
               team_200, team_100
        FROM esports_data
        WHERE platformgameid = ?
    ''', (platform_game_id,))

    # Fetch the results and create a dictionary
    row = cursor.fetchone()
    if row:
        participant_ids = [row[i] for i in range(10)]
        team_200 = row[10]
        team_100 = row[11]
        result_dict = {
            'participant_ids': participant_ids,
            'team_200': team_200,
            'team_100': team_100
        }
    else:
        result_dict = None

    # Close the connection
    conn.close()

    return result_dict

def get_team_info(event):
    if event["eventType"] != "game_info":
        raise ValueError("Tried to get team info from a non game_info event")

    participants = event["participants"]
    res = get_participants_and_teams(event["platformGameId"])
    team_info = {
        "team_100" : {
            "team_id" : res["team_100"],
            "players" : []
        },
        "team_200" : {
            "team_id" : res["team_200"],
            "players" : []
        }
    }

    team_100_players, team_200_players = [], []
    for p in participants:
        # res["participant_ids"] is ordered, particpantId 1 is index 0, 2 is 1 and so on
        team_info[f'team_{p["teamID"]}']["players"].append(res["participant_ids"][p["participantID"]-1])

    return team_info

def get_relevant_data(event):
    data = dict()

    data["eventTime"] = event["eventTime"]
    data["eventType"] = event["eventType"]
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
        

    return data

# Function to group events into 5-minute intervals
def group_events_by_interval(events):
    interval_length = 5  # in minutes
    grouped_events = []
    current_interval_start = None
    current_interval_events = []

    # skip the first game_info event
    for i in range(1, len(events)):
        event = events[i]
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
    team_info = get_team_info(events[0])
    grouped_events = group_events_by_interval(events)

    output_path = os.path.join(os.path.abspath(os.getcwd()), 'intervals/')
    if not os.path.exists(output_path):
        cwd = os.path.abspath(os.getcwd())
        os.makedirs(output_path)

    output_file = os.path.join(output_path, file_name)

    obj = {
        "team_info" : team_info,
        "intervaled_events" : grouped_events
    }
    with open(output_file, 'w') as data_file:
        json.dump(obj, data_file, indent=4)
    
    print(f"Done writing {output_file}...")

cwd = os.path.abspath(os.getcwd())
path = os.path.join(cwd, 'games/')
for file in os.listdir(path):
    get_events_from_file(file, path)
