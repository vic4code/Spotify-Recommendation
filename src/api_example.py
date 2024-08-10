import json
import os
from typing import Any, Dict, List, Union

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def convert_to_type_structure(d: Any) -> Union[Dict[str, Any], str]:
    if isinstance(d, dict):
        type_structure = {}
        for key, value in d.items():
            if isinstance(value, (dict, list)):
                type_structure[key] = convert_to_type_structure(value)
            else:
                type_structure[key] = type(value).__name__
        return type_structure
    elif isinstance(d, list):
        if not d:
            return "List[Any]"
        first_type = type(d[0]).__name__
        if all(isinstance(item, dict) for item in d):
            return [convert_to_type_structure(d[0])]
        elif all(isinstance(item, str) for item in d):
            return "List[str]"
        elif all(isinstance(item, int) for item in d):
            return "List[int]"
        elif all(isinstance(item, float) for item in d):
            return "List[float]"
        elif all(isinstance(item, bool) for item in d):
            return "List[bool]"
        elif all(isinstance(item, type(d[0])) for item in d):
            return f"List[{first_type}]"
        else:
            return "List[Mixed]"
    else:
        return type(d).__name__


if __name__ == "__main__":

    # Set credential
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    auth_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Search for a track by track name and return the first result
    track_name = "Perfect Night"
    results = sp.search(q=track_name, type="track", limit=1)
    track_type_structure = convert_to_type_structure(results)
    formatted_track_type_structure = json.dumps(
        track_type_structure, indent=4, ensure_ascii=False
    )
    print("Track", formatted_track_type_structure)

    # Search the artist of the track
    artist_id = results["tracks"]["items"][0]["artists"][0]["id"]
    artist = sp.artist(artist_id)
    artist_type_structure = convert_to_type_structure(artist)
    formatted_artist_type_structure = json.dumps(
        artist_type_structure, indent=4, ensure_ascii=False
    )
    print("Artist", formatted_artist_type_structure)

    # Search a playlist
    username = "11100022591"
    playlist_name = "<3"
    playlists = sp.user_playlists(username)
    for playlist in playlists["items"]:
        if playlist["name"] == playlist_name:
            playlist_type_structure = convert_to_type_structure(playlist)
            formatted_playlist_type_structure = json.dumps(
                playlist_type_structure, indent=4, ensure_ascii=False
            )
            print("Playlist", formatted_playlist_type_structure)
            break

    breakpoint()
