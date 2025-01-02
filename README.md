# podcast-reaper

## Origin

Quickly created using chatgpt and a few lines of code.
https://chatgpt.com/share/677556f1-40dc-8005-8d12-46d8dbd8b1a7

Originally to convert the awsome podcast by Urbain and Clément, "Plutot caustique" to text.
Can be used on others podcasts.

License APACHE 2.0 fill free to use and modify.

## Usage

1. Install the requirements

  ```bash
  pip install -r requirements.txt
  ```

2. Run the script
   The first time you run the script, you need to provide the url and the language of the podcast.

  ```bash
  python podcast_downloader.py --url "https://feeds.acast.com/public/shows/plutot-caustique" --language "fr"
  ```

3. Re Run the script
    The next time you run the script, you can use the config file to avoid providing the url and the language.
  ```bash
  python podcast_downloader.py --file config.json
  ```