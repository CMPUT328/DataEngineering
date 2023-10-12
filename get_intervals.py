import json
from datetime import datetime, timedelta
import os
import sqlite3

prev_stats_update = None


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
        "team_100": {
            "team_id": res["team_100"],
            "players": []
        },
        "team_200": {
            "team_id": res["team_200"],
            "players": []
        }
    }

    team_100_players, team_200_players = [], []
    for p in participants:
        # res["participant_ids"] is ordered, particpantId 1 is index 0, 2 is 1 and so on
        team_info[f'team_{p["teamID"]}']["players"].append(
            res["participant_ids"][p["participantID"]-1])

    return team_info


def get_relevant_data(event):
    data = dict()

    data["eventTime"] = event["eventTime"]
    data["eventType"] = event["eventType"]

    if event["eventType"] == "building_destroyed":
        key_list = ["teamID", "buildingType", "lane", "turretTier"]
        for k in key_list:
            try: 
                data[k] = event[k]
            except KeyError:
                pass

    # there is also champion_kill special, which is multikills and first blood
    if event["eventType"] == "champion_kill":
        key_list = ["victimTeamID", "victim",
                    "killerTeamID", "shutdownBounty", "bounty"]
        for k in key_list:
            if k == "killerTeamID":
                data['teamID'] = event[k]
            else:
                data[k] = event[k]

        # how many players killed the champion
        # can store the people giving assist if we want
        data["num_attackers"] = len(event["assistants"]) + 1

    # if it's a dragon there is an extra key about the type of dragon, can add if we want
    if event["eventType"] == "epic_monster_kill":
        key_list = ["killerTeamID", "killer",
                    "monsterType", "inEnemyJungle"]
        for k in key_list:
            if k == "killerTeamID":
                data['teamID'] = event[k]
            else:
                data[k] = event[k]

        # how many players killed the monster
        data["num_attackers"] = len(event["assistants"]) + 1

    if event["eventType"] == "turret_plate_destroyed":
        data['teamID'] = event['teamID']

    if event["eventType"] == "game_end":
        data['teamID'] = event['winningTeam']

    if event["eventType"] == "stats_update":
        global prev_stats_update
        if prev_stats_update is None:
            prev_stats_update = event
        else:
            prev_participants = prev_stats_update["participants"]
            cur_participants = event["participants"]
            for i in range(10):
                cur, prev = prev_participants[i], cur_participants[i]

                # ultimate used
                if cur["ultimateCooldownRemaining"] > 0 and prev["ultimateCooldownRemaining"] == 0:
                    assert(cur["participantID"] == prev["participantID"])
                    data.update(
                        {
                            "eventInfo": "ultimateUsed",
                            "casterID": cur["participantID"],
                            "teamID": cur["teamID"]
                        }
                    )

            prev_stats_update = event

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
        event_time = datetime.fromisoformat(
            event["eventTime"][:-1])  # Parse event time
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
        "team_info": team_info,
        "intervaled_events": grouped_events
    }
    with open(output_file, 'w') as data_file:
        json.dump(obj, data_file, indent=4)

    print(f"Done writing {output_file}...")


cwd = os.path.abspath(os.getcwd())
path = os.path.join(cwd, 'games/')
for file in os.listdir(path):
    get_events_from_file(file, path)
