import json
import os
import glob


def extract_game(path):


    
        
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
    parts = path.split("/")
    name = parts[1][:len(parts[1])-5]+"_short.json"
    if not os.path.exists('extracted_games'):
        os.makedirs('extracted_games')
    with open('extracted_games/' + name, 'w') as f:
        json.dump(data, f, indent=4)

