import argparse
import json
import logging
import os
import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

# Set up logging
logging.basicConfig(filename="spotify_requests.log", level=logging.INFO)

if __name__ == "__main__":

    # Set credentials
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    auth_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    with open("./data/modeling/train.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    additional_data = {}

    for artist_uri, index in tqdm(data["artist_uri2id"].items()):
        try:
            artist = sp.artist(artist_uri)
            additional_data[artist_uri] = artist
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Error fetching data for {artist_uri}: {e}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            continue

        # Adding a delay to avoid hitting rate limits
        time.sleep(0.1)  # Adjust sleep time as necessary

    # Save the augmented data
    with open("./data/modeling/artist_uri2profile.json", "w", encoding="utf-8") as file:
        json.dump(additional_data, file, ensure_ascii=False, indent=4)
