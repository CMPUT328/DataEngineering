import json
import random

# Load data from the JSON file
with open('matches_league.json', 'r') as f:
    data = json.load(f)

# The original dictionary
original_dict = {
    '98767991299243165': 'LCS',
    '109511549831443335': 'LCS Challengers',
    '109518549825754242': 'LCS Challengers Qualifiers',
    '107898214974993351': 'College Championship',
    '98767991332355509': 'CBLOL',
    '98767991310872058': 'LCK',
    '98767991355908944': 'LCL',
    '105709090213554609': 'LCO',
    '98767991302996019': 'LEC',
    '98767991349978712': 'LJL',
    '101382741235120470': 'LLA',
    '98767991314006698': 'LPL',
    '104366947889790212': 'PCS',
    '98767991343597634': 'TCL',
    '107213827295848783': 'VCS',
    '98767991325878492': 'MSI',
    '98767975604431411': 'Worlds',
    '98767991295297326': 'All-Star Event',
    '100695891328981122': 'EMEA Masters',
    '105266103462388553': 'La Ligue Française',
    '105266098308571975': 'NLC',
    '107407335299756365': 'Elite Series',
    '105266101075764040': 'Liga Portuguesa',
    '105266094998946936': 'PG Nationals',
    '105266088231437431': 'Ultraliga',
    '105266074488398661': 'SuperLiga',
    '105266091639104326': 'Prime League',
    '105266106309666619': 'Hitpoint Masters',
    '105266111679554379': 'Esports Balkan League',
    '105266108767593290': 'Greek Legends League',
    '109545772895506419': 'Arabian League',
    '108203770023880322': 'LCK Academy',
    '106827757669296909': 'LJL Academy',
    '98767991335774713': 'LCK Challengers',
    '105549980953490846': 'CBLOL Academy',
    '110371976858004491': 'North Regional League',
    '110372322609949919': 'South Regional League',
    '108001239847565215': 'TFT Rising Legends'
}

# The hypothetical league rankings
league_ranking = {
    'Worlds': 1,
    'MSI': 2,
    'LEC': 3,
    'LCK': 4,
    'LCS': 5,
    'LPL': 6,
    'CBLOL': 7,
    'LLA': 8,
    'LJL': 9,
    'LCL': 10,
    'TCL': 11,
    'VCS': 12,
    'PCS': 13,
    'LCO': 14,
    'LCS Challengers': 15,
    'LCS Challengers Qualifiers': 16,
    'LCK Challengers': 17,
    'LCK Academy': 18,
    'LJL Academy': 19,
    'CBLOL Academy': 20,
    'EMEA Masters': 21,
    'All-Star Event': 22,
    'College Championship': 23,
    'Prime League': 24,
    'NLC': 25,
    'La Ligue Française': 26,
    'Ultraliga': 27,
    'SuperLiga': 28,
    'PG Nationals': 29,
    'Liga Portuguesa': 30,
    'Hitpoint Masters': 31,
    'Esports Balkan League': 32,
    'Greek Legends League': 33,
    'Elite Series': 34,
    'TFT Rising Legends': 35,
    'North Regional League': 36,
    'South Regional League': 37,
    'Arabian League': 38
}

# Sorting the original dictionary based on the hypothetical league rankings
sorted_dict = dict(sorted(original_dict.items(), key=lambda item: league_ranking.get(item[1], float('inf'))))

# Construct the game_results array directly without mapping
game_results = []
for match in data:
    team1 = match["teams"][0]
    team2 = match["teams"][1]
    winner = 1 if match["winner"] == team1 else 0
    game_results.append((team1, team2, winner, match["league"]))

# Split the data into training and test sets
random.shuffle(game_results)
split_index = int(1 * len(game_results))
training_data = game_results[:split_index]
test_data = game_results[split_index:]

# Get unique team ids
unique_teams = {team for match in data for team in match["teams"]}

# Initialize strengths
team_strengths = {unique_team: 1000 for unique_team in unique_teams}

k1 = 40
k2 = 30

def get_index_of_key(d, target_key):
    for index, key in enumerate(d.keys()):
        if key == target_key:
            return index
    return None

# Adjust strengths based on training data
for team1, team2, result, league_id in training_data:

    if str(league_id) not in original_dict:
        continue

    dr = team_strengths[team1] - team_strengths[team2]

    index = get_index_of_key(sorted_dict, str(league_id))
    k1 = 30 + (37 - index)
    k2 = 30 + (37 - index)

    # Update strength for team 1
    adjustment_team1 = k1 * (result - 1 / (pow(10, (-dr/400)) + 1))
    team_strengths[team1] += adjustment_team1

    def toggle(value):
      if value == 1:
          return 0
      else:
          return 1
    
    # Since game_result is binary (1 if team1 wins, 0 otherwise), 
    # the adjustment for team2 is simply the negative of team1's adjustment.
    adjustment_team2 = k2 * (toggle(result) - 1 / (pow(10, (dr/600)) + 1))
    team_strengths[team2] += adjustment_team2

# for i, score in enumerate(team_strengths):
#     print(i)
#     print(team_strengths[score])

# average_value = sum(team_strengths.values()) / len(team_strengths)
# print(average_value)
# print(min(team_strengths.values()))
# print(max(team_strengths.values()))

sorted_strength = dict(sorted(team_strengths.items(), key=lambda item: item[1], reverse=True))

# print(sorted_strength)

# Array of team_id to look for
team_ids = sorted_strength.keys()

with open('teams.json', 'r') as f:
    teams_data = json.load(f)

# Extracting team names
for team_id, team_strength in sorted_strength.items():
    for team in teams_data:
        if str(team["team_id"]) == str(team_id):
            print(f"{team['name']}: {team_strength:.2f}")

# # Test accuracy using test data
# correct_predictions = 0
# total_predictions = 0
# for team1, team2, actual_result, league_id in test_data:
#     if (abs(team_strengths[team1] - team_strengths[team2]) > 200):
#       predicted_result = 1 if team_strengths[team1] > team_strengths[team2] else 0
#       correct_predictions += 1 if (predicted_result == actual_result) else 0
#       total_predictions += 1

# accuracy = correct_predictions / total_predictions

# print(f"Accuracy on test data: {accuracy:.2%}")
# print(correct_predictions)
# print(total_predictions)