from datetime import datetime

import requests
import xml.etree.ElementTree as ET
import json

# RSS feed URL
rss_url = "https://feeds.acast.com/public/shows/plutot-caustique"

# Retrieve RSS feed data
response = requests.get(rss_url)
if response.status_code != 200:
    print(f"Error retrieving data: {response.status_code}")
    exit()

# Parse the RSS feed
root = ET.fromstring(response.content)

# Extract episodes
episodes = []
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
                   .replace(' ', '_')
                   .replace('"', ''))
    pub_date = item.find("pubDate").text
    try:
        pub_date_formatted = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {pub_date}")

    enclosure = item.find("enclosure")
    if enclosure is not None:
        mp3_url = enclosure.attrib.get("url")
        episodes.append({"url": mp3_url,
                         "episode": title,
                         "date": pub_date_formatted,
                         "cleanTitle": clean_title,
                         "fileName": f"{pub_date_formatted}-{clean_title}.mp3"
                         })

# Write data to a JSON file
output_file = "episodes.json"
with open(output_file, "w", encoding="utf-8") as file_handler:
    json.dump(episodes,
              file_handler,
              indent=2,
              ensure_ascii=False)

print(f"JSON file created: {output_file}")
