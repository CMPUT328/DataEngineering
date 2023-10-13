import json
import os
import glob

### The code takes the game json files and creates a extracted_games folder, and store {gamenames}_short.json


# Directory of the games. Change it for yourself and remember \\ or \ or / at the end
directory = "raw_data\\scripts\\games\\"

paths = glob.glob(directory + '*.json')

for path in paths:
    
    with open(path, 'r') as f:
        game_obj = json.load(f)

    data = []
    for event in game_obj:
        if event["eventType"] == "stats_update":
            if event["gameTime"] <= 900000:
                for player in event["participants"]:
                    player["stats"] = [stat for stat in player["stats"] if not ('PINGS' in stat["name"])]
                    for i in range(1,4):
                        player.pop("ability{}Name".format(i))
                        player.pop("ability{}CooldownRemaining".format(i))
                temp1 = event
            else:
                break
    data.append(temp1)

    end_game = game_obj[len(game_obj)-2]

    for player in end_game["participants"]:
        player["stats"] = [stat for stat in player["stats"] if not 'PINGS' in stat["name"]]
        for i in range(1,4):
            player.pop("ability{}Name".format(i))
            player.pop("ability{}CooldownRemaining".format(i))
            
    data.append(end_game)
    parts = path.split("\\")
    name = parts[3][:len(parts[3])-5]+"_short.json"
    with open('extracted_games\\' + name, 'w') as f:
        json.dump(data, f, indent=4)

