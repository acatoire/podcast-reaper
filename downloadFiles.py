import os
import json
import requests

# Path to the JSON file
json_file_path = "episodes.json"

# Destination folder for downloaded files
download_folder = "./downloads"
os.makedirs(download_folder, exist_ok=True)

# Load data from the JSON file
with open(json_file_path, "r", encoding="utf-8") as json_file:
    episodes = json.load(json_file)

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