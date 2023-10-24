import json

# Read the JSON data from the file
with open('tournaments.json', 'r') as file:
    data = json.load(file)

# Convert the data
converted = []

for tournament in data:
    for stage in tournament["stages"]:
        for section in stage["sections"]:
            for match in section["matches"]:
                for game in match["games"]:
                    team1 = game["teams"][0]
                    team2 = game["teams"][1]
                    try:
                        if (team1["result"]["outcome"] == "win" or team1["result"]["outcome"] == "loss"):
                            winner_id = team1["id"] if team1["result"]["outcome"] == "win" else team2["id"]
                            
                            game_data = {
                                "teams": [team1["id"], team2["id"]],
                                "winner": winner_id,
                                "league": tournament["leagueId"],
                                "tournament": tournament["id"],
                                "section": section["name"],
                                "startDate": tournament["startDate"]
                            }
                            
                            converted.append(game_data)
                    except Exception:
                        continue

# Write the converted data to a new JSON file
with open('game_results_v2.json', 'w') as file:
    json.dump(converted, file, indent=4)

