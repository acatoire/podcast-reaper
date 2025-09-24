from datetime import datetime
import requests
import xml.etree.ElementTree as ElementTree
import json
import os

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

input_path = input("Enter the path to the existing containing episodes.json: ").strip()
input_json_path = os.path.join(input_path, "episodes.json")

with open(input_json_path, "r", encoding="utf-8") as f:
    podcast_info = json.load(f)

#
rss_url = podcast_info['listen']['acast']
if not rss_url:
    rss_url = podcast_info['listen']['ausha']
if not rss_url:
    rss_url = podcast_info['listen']['feedburner']
if not rss_url: # TODO be compatible with audion
    rss_url = podcast_info['listen']['audion']

if not rss_url:
    print("No valid RSS URL found in Valid RSS URLs are [acast, ausha, feedburner] fields.")
    exit()
else:
    print(f"Using RSS URL: {rss_url}")

# Collect all existing episode URLs from all seasons
existing_urls = set()
for saison in podcast_info.get("Saisons", []):
    for ep in saison.get("episodes", []):
        url = ep.get("url")
        if url:
            existing_urls.add(url)

response = requests.get(rss_url)
if response.status_code != 200:
    print(f"Error retrieving data: {response.status_code}")
    exit()

root = ElementTree.fromstring(response.content)

new_episodes = []
for item in root.findall("./channel/item"):
    title = item.find("title").text
    clean_title = (title
                   .replace(' : ', '-')
                   .replace(': ', '-')
                   .replace("'", '_')
                   .replace("*", '_')
                   .replace("?", '_')
                   .replace("!", '_')
                   .replace(',', '')
                   .replace('...', '')
                   .replace(' ', '_')
                   .replace('"', ''))
    pub_date = item.find("pubDate").text
    description = item.find("description").text
    try:
        pub_date_formatted = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
    except ValueError:
        try:
            pub_date_formatted = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {pub_date}")

    enclosure = item.find("enclosure")
    if enclosure is not None:
        mp3_url = enclosure.attrib.get("url")
        if mp3_url not in existing_urls:
            new_episodes.append({
                "url": mp3_url,
                "episode": title,
                "description": description,
                "date": pub_date_formatted,
                "cleanTitle": clean_title,
                "fileName": f"{pub_date_formatted}-{clean_title}.mp3",
                "label": ""
            })

# Write only new episodes as a new season in the same JSON structure
if new_episodes:
    new_season = {
        "name": "new episodes",
        "episodes": new_episodes
    }
    # Copy the original structure and append the new season
    updated_json = podcast_info.copy()
    saisons = list(updated_json.get("Saisons", []))
    saisons.append(new_season)
    updated_json["Saisons"] = saisons
else:
    updated_json = podcast_info

with open(input_json_path, "w", encoding="utf-8") as file_handler:
    json.dump(updated_json, file_handler, indent=2, ensure_ascii=False)

print(f"JSON file updated: {input_json_path}")
