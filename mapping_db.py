import sqlite3
import json

with open('esports-data/mapping_data.json', 'r') as data_file:
    json_data = data_file.read()

json_objects = json.loads(json_data)

# Create a connection to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('mapping_data.db')
cursor = conn.cursor()

# Create a table in the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS esports_data (
        esportsgameid TEXT,
        platformgameid TEXT,
        team_200 TEXT,
        team_100 TEXT,
        participant_1 TEXT,
        participant_2 TEXT,
        participant_3 TEXT,
        participant_4 TEXT,
        participant_5 TEXT,
        participant_6 TEXT,
        participant_7 TEXT,
        participant_8 TEXT,
        participant_9 TEXT,
        participant_10 TEXT
    )
''')

# Insert data into the table
for obj in json_objects:
    esports_game_id = obj['esportsGameId']
    platform_game_id = obj['platformGameId']
    team_200 = obj['teamMapping'].get('200', '')
    team_100 = obj['teamMapping'].get('100', '')
    participants = [obj['participantMapping'].get(str(i), '') for i in range(1, 11)]

    cursor.execute('''
        INSERT INTO esports_data (esportsgameid, platformgameid, team_200, team_100, participant_1, participant_2, participant_3, participant_4, participant_5, participant_6, participant_7, participant_8, participant_9, participant_10)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (esports_game_id, platform_game_id, team_200, team_100, *participants))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")