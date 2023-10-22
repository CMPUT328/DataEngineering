import json

# Read the team strengths
with open('ranked_teams_with_score.json', 'r') as file:
    team_strengths_data = json.load(file)

# Create a dictionary for quick lookup of team strengths
team_strengths = {team["team_id"]: team["Strength"] for team in team_strengths_data}

# Read the game results data
with open('game_results_v2.json', 'r') as file:
    game_results_data = json.load(file)

# Dictionary to store the sum of team strengths and the number of teams for each tournament
tournament_strength_sums = {}
tournament_team_counts = {}

for game in game_results_data:
    tournament_id = game["tournament"]
    tournament_name = game["section"]
    if tournament_id not in tournament_strength_sums:
        tournament_strength_sums[tournament_id] = 0
        tournament_team_counts[tournament_id] = 0
    
    for team_id in game["teams"]:
        if team_id in team_strengths:
            tournament_strength_sums[tournament_id] += team_strengths[team_id]
            tournament_team_counts[tournament_id] += 1

# Calculate average strengths
tournament_avg_strengths = {}
for tournament_id in tournament_strength_sums:
    tournament_avg_strengths[tournament_id] = tournament_strength_sums[tournament_id] / tournament_team_counts[tournament_id]

# Write to a JSON file
with open('tournament_avg_strengths.json', 'w') as file:
    json.dump(tournament_avg_strengths, file, indent=4)
