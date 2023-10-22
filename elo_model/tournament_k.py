import json

# Read the data from tournament_avg_strengths.json
with open('tournament_avg_strengths.json', 'r') as input_file:
    data = json.load(input_file)

min_value = min(data.values())
max_value = max(data.values())

new_min = 10
new_max = 100

normalized_data = {}
for key, value in data.items():
    normalized_value = ((value - min_value) / (max_value - min_value)) * (new_max - new_min) + new_min
    normalized_data[key] = normalized_value

# Process the data as required
# For now, I'll just take the data as is, but you can modify it as needed
output_data = data  # Replace this with any processing you'd like

# Write the data to tournament_k.json
with open('tournament_k.json', 'w') as output_file:
    json.dump(output_data, output_file, indent=4)
