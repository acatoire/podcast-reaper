# Podcast Reaper

A tool for downloading, processing, and displaying podcast content.

## Origin

Quickly created using ChatGPT and a few lines of code.
https://chatgpt.com/share/677556f1-40dc-8005-8d12-46d8dbd8b1a7

Originally to convert the awesome podcast by Urbain and Clément, "Plutot Caustique" to text.
Can be used on other podcasts.

License APACHE 2.0 - feel free to use and modify.

## Features

- **Python Scripts**: Download and process podcast episodes
- **Website**: Simple, responsive website to browse and listen to podcasts without JavaScript frameworks

## Python Script Usage

1. Install the requirements

  ```bash
  pip install -r app/requirements.txt
  ```

2. Run the script
   The first time you run the script, you need to provide the URL and the language of the podcast.

  ```bash
  python podcast_downloader.py --url "https://feeds.acast.com/public/shows/plutot-caustique" --language "fr"
  ```

3. Re-run the script
   The next time you run the script, you can use the config file to avoid providing the URL and the language.
  ```bash
  python podcast_downloader.py --file config.json
  ```

## Website Usage

The repository includes a simple, responsive website for browsing and listening to podcasts:

1. Open `index.html` in a web browser to view available podcasts
2. Click on a podcast to view its episodes
3. Click on an episode to view details and listen to it

### Website Structure

- `index.html` - Main page that lists available podcasts
- `podcast.html` - Podcast detail page that displays episodes and their details
- `styles.css` - Stylesheet for the website
- `podcasts/` - Directory containing podcast data

### Adding a New Podcast to the Website

1. Create a new directory in the `podcasts/` folder with the podcast name (use lowercase and underscores for spaces)
2. Create an `episodes.json` file in the new directory with episode data
3. Add a new podcast card to the `index.html` file

The website is responsive and works on both desktop and mobile devices.
