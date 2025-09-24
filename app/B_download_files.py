import os
import json
import requests

# The JSON file must have this structure:
# {
#   "name": "...",
#   "description": "...",
#   "authors": "...",
#   "listen": [
#     {"name": "apple", "link": "..."},
#     {"name": "acast", "link": "..."},
#     {"name": "spotify", "link": "..."},
#     {"name": "deezer", "link": "..."}
#   ],
#   "Saisons": [
#     {
#       "name": "...",
#       "episodes": [
#         {"url": "...", ...}
#       ]
#     }
#   ]
# }

root_folder = input("Enter the path to the folder containing episodes.json: ").strip()

input_json_path = os.path.join(root_folder, 'episodes.json')
with open(input_json_path, "r", encoding="utf-8") as f:
    podcast_info = json.load(f)

# Destination folder for downloaded files
download_folder = os.path.join(os.path.dirname(input_json_path), "downloads")
os.makedirs(download_folder, exist_ok=True)

# Get the new season content
episodes = next((saison["episodes"] for saison in podcast_info["Saisons"] if saison["name"] == "new episodes"), [])

if not episodes:
    print("No 'new episodes' season found or it is empty.")
    exit()

# Download each file
for episode in episodes:
    url = episode["url"]
    filename = episode["fileName"]
    filepath = os.path.join(download_folder, filename)

    if os.path.exists(filepath):
        print(f"File already exists: {filename}")
        continue

    print(f"Downloading: {filename} from {url}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors

        # Write the file
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"File downloaded: {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")

print("Download complete.")