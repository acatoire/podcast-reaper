import os
import json
import re

# Paths
input_path = input("Enter the path to the existing containing episodes.json: ").strip()
input_json_path = os.path.join(input_path, "episodes.json")
info_files_dir = os.path.join(input_path, "turbo")

# Load the JSON data
with open(input_json_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Regex to extract duration from the info file
duration_regex = r'File: .* - .* - (\d+\.\d+) minutes'

# Iterate through seasons and episodes
for season in data.get('Saisons', []):
    for episode in season.get('episodes', []):
        # Build the path to the corresponding info file
        date = episode['date']
        clean_title = episode['cleanTitle']
        info_file_path = os.path.join(info_files_dir, date, f"{date}-info.txt")

        # Check if the info file exists
        if os.path.exists(info_file_path):
            with open(info_file_path, 'r', encoding='utf-8') as info_file:
                content = info_file.read()
                # Extract the duration
                match = re.search(duration_regex, content)
                if match:
                    duration = float(match.group(1))
                    # Keep only integer part of the duration
                    duration = int(duration)
                    # Update the episode with the duration
                    episode['duration'] = duration
                    print(f"Updated {episode['episode']} with duration: {duration} minutes")

# Save the updated JSON data
with open(input_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

print("Episodes updated with durations.")