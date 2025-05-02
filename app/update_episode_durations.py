import os
import json
import csv

def format_duration(milliseconds):
    """Convert milliseconds to a human-readable duration format (MM:SS)."""
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"

def update_episode_durations(podcast_name):
    """
    Update episode durations in episodes.json by extracting the timestamp of the last speech from TSV files.
    
    Args:
        podcast_name (str): Name of the podcast folder (e.g., 'pardon_gpt')
    """
    # Path to the episodes.json file
    episodes_json_path = os.path.join('podcasts', podcast_name, 'episodes.json')
    
    # Check if the episodes.json file exists
    if not os.path.exists(episodes_json_path):
        print(f"Error: {episodes_json_path} does not exist.")
        return
    
    # Load the episodes.json file
    with open(episodes_json_path, 'r', encoding='utf-8') as f:
        episodes_data = json.load(f)
    
    # Initialize a counter for updated episodes
    updated_count = 0
    
    # Iterate through seasons and episodes
    for season in episodes_data.get('Saisons', []):
        for episode_list in season.get('episodes', []):
            # Handle both list of episodes and direct episode objects
            episodes = episode_list if isinstance(episode_list, list) else [episode_list]
            
            for episode in episodes:
                # Get the episode date
                date_str = episode.get('date')
                if not date_str:
                    continue
                
                # Construct the path to the TSV file
                tsv_path = os.path.join('podcasts', podcast_name, 'turbo', date_str, f"{date_str}.tsv")
                
                # Check if the TSV file exists
                if not os.path.exists(tsv_path):
                    print(f"Warning: TSV file not found for episode {episode.get('episode')} ({date_str})")
                    continue
                
                try:
                    # Read the TSV file to find the last timestamp
                    with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
                        # Skip the header row
                        next(tsv_file)
                        
                        # Read all lines to find the last one with valid timestamps
                        last_end_time = 0
                        for line in csv.reader(tsv_file, delimiter='\t'):
                            if len(line) >= 2 and line[1].strip():
                                try:
                                    end_time = int(line[1])
                                    if end_time > last_end_time:
                                        last_end_time = end_time
                                except ValueError:
                                    # Skip lines with non-integer timestamps
                                    continue
                    
                    # If we found a valid end time, update the episode
                    if last_end_time > 0:
                        # Add or update the duration field
                        episode['duration'] = last_end_time
                        episode['duration_formatted'] = format_duration(last_end_time)
                        updated_count += 1
                        print(f"Updated episode: {episode.get('episode')} - Duration: {episode.get('duration_formatted')}")
                    else:
                        print(f"Warning: No valid end time found for episode {episode.get('episode')} ({date_str})")
                
                except Exception as e:
                    print(f"Error processing TSV file for episode {episode.get('episode')} ({date_str}): {str(e)}")
    
    # Save the updated episodes.json file
    with open(episodes_json_path, 'w', encoding='utf-8') as f:
        json.dump(episodes_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nUpdated {updated_count} episodes in {episodes_json_path}")

if __name__ == "__main__":
    import sys
    
    # Check if a podcast name was provided as a command-line argument
    if len(sys.argv) > 1:
        podcast_name = sys.argv[1]
    else:
        # Default to 'pardon_gpt' if no podcast name is provided
        podcast_name = 'pardon_gpt'
    
    print(f"Updating episode durations for podcast: {podcast_name}")
    update_episode_durations(podcast_name)
    print("Done!")