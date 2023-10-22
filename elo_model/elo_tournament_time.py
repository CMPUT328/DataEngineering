import json

# Load data from the game_results_v2.json file
with open('game_results_v2.json', 'r') as f:
    data = json.load(f)

# Load team strengths from the tournament_avg_strengths.json file
with open('tournament_avg_strengths.json', 'r') as f:
    tournament_strengths = json.load(f)

with open('tournament_k.json', 'r') as f:
    tournament_k = json.load(f)

# Construct the game_results array directly without mapping
game_results = []
for match in data:
    team1 = match["teams"][0]
    team2 = match["teams"][1]
    winner = 1 if match["winner"] == team1 else 0
    game_results.append((team1, team2, winner, match["tournament"], match["section"], match["startDate"]))

# Split the data into training and test sets
game_results.sort(key=lambda x: x[5])
split_index = int(1 * len(game_results))
training_data = game_results[:split_index]
test_data = game_results[split_index:]

# Get unique team ids
unique_teams = {team for match in data for team in match["teams"]}

def get_tournaments_by_team(team_id, game_results):
    tournaments = [result[3] for result in game_results if team_id in (result[0], result[1])]
    return tournaments

# Initialize strengths using the average strength of tournaments a team has played in
team_strengths = {}

for unique_team in unique_teams:
    tournaments_played = get_tournaments_by_team(unique_team, game_results)
    if not tournaments_played:  # If the team hasn't played any matches
        team_strengths[unique_team] = 1000
        continue

    total_strength = sum(tournament_strengths.get(tournament, 1000) for tournament in tournaments_played)
    avg_strength = total_strength / len(tournaments_played)
    team_strengths[unique_team] = avg_strength

# Adjust strengths based on training data
for team1, team2, result, tournament_id, section_name, date in training_data:

    dr = team_strengths[team1] - team_strengths[team2]

    k1 = tournament_k.get(tournament_id)
    k2 = tournament_k.get(tournament_id)

    if (section_name == "Playoffs" or section_name == "knockouts"):
        k1 *= 1.2
        k2 *= 1.2

    # Update strength for team 1
    adjustment_team1 = k1 * (result - (1 / (pow(10, (-dr/400)) + 1)))
    team_strengths[team1] += adjustment_team1

    def toggle(value):
        if value == 1:
            return 0
        else:
            return 1
    
    # Since game_result is binary (1 if team1 wins, 0 otherwise), 
    # the adjustment for team2 is simply the negative of team1's adjustment.
    adjustment_team2 = k2 * (toggle(result) - (1 / (pow(10, (dr/600)) + 1)))
    team_strengths[team2] += adjustment_team2

sorted_strength = dict(sorted(team_strengths.items(), key=lambda item: item[1], reverse=True))

with open('teams.json', 'r') as f:
    teams_data = json.load(f)

# Extracting team names
for team_id, team_strength in sorted_strength.items():
    for team in teams_data:
        if str(team["team_id"]) == str(team_id):
            print(f"{team['name']}: {team_strength:.2f}")

# Create a list to hold the ranked teams data
ranked_teams = []

# Loop through the sorted strength
for rank, (team_id, team_strength) in enumerate(sorted_strength.items(), 1):
    for team in teams_data:
        if str(team["team_id"]) == str(team_id):
            ranked_teams.append({
                "team_id": team_id,
                "name": team["name"],
                "rank": rank,
                "Strength": team_strength,
            })
            break

# Convert the ranked_teams list to JSON
with open("ranked_teams_with_score_v2.json", "w", encoding="utf-8") as file:
    json.dump(ranked_teams, file, ensure_ascii=False, indent=4)

# Test accuracy using test data
correct_predictions = 0
total_predictions = 0
for team1, team2, actual_result, tournament_id, section_name, date in training_data:
    if (abs(team_strengths[team1] - team_strengths[team2]) > 0):
      predicted_result = 1 if team_strengths[team1] > team_strengths[team2] else 0
      correct_predictions += 1 if (predicted_result == actual_result) else 0
      total_predictions += 1

accuracy = correct_predictions / total_predictions

print(f"Accuracy on test data: {accuracy:.2%}")
print(correct_predictions)
print(total_predictions)