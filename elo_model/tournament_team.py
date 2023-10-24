import json

# Read the data from the file
with open('game_results_v2.json', 'r') as file:
    data = json.load(file)

# Create a dictionary with tournament IDs as keys
tournament_teams = {}

for game in data:
    tournament_id = game["tournament"]
    
    # Check if tournament ID already exists in the dictionary
    if tournament_id not in tournament_teams:
        tournament_teams[tournament_id] = set()  # Using a set to avoid duplicate teams
    
    # Add the teams to the set
    for team in game["teams"]:
        tournament_teams[tournament_id].add(team)

# Convert the sets to lists for JSON serialization
for tournament_id, teams in tournament_teams.items():
    tournament_teams[tournament_id] = list(teams)

# Write to a JSON file
with open('tournaments_and_teams.json', 'w') as file:
    json.dump(tournament_teams, file, indent=4)
