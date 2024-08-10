# Spotify-Recommendation

## Spotify Million Playlist Dataset Exploration
- AiCrowd CLI installation
```
pip install -U aicrowd-cli==0.1 > /dev/null
aicrowd login --api-key <api-key>
aicrowd dataset list --challenge spotify-million-playlist-dataset-challenge
```
- List the datasets for the challenge
```
Datasets for challenge #277                                                                                                                                   
┌───┬─────────────────────────────────────────────────────────┬─────────────┬───────────┐                                                                                                    
│ # │ Title                                                   │ Description │      Size │                                                                                                    
├───┼─────────────────────────────────────────────────────────┼─────────────┼───────────┤                                                                                                    
│ 0 │ Resourcesspotify_million_playlist_dataset.zip           │ -           │   5.79 GB │                                                                                                    
│ 1 │ Resourcesspotify_million_playlist_dataset_challenge.zip │ -           │ 113.33 MB │                                                                                                    
└───┴─────────────────────────────────────────────────────────┴─────────────┴───────────┘    
```
- Download the datasets with cli
```
aicrowd dataset download --challenge spotify-million-playlist-dataset-challenge 0 1
```
- Randomly split them into train and test splits.
```bash
bash data/data_split.sh 
```
- An example of the playlist in MPD Challenge.
```json
{
   "name":"Throwbacks",
   "collaborative":"false",
   "pid":0,
   "modified_at":1493424000,
   "num_tracks":52,
   "num_albums":47,
   "num_followers":1,
   "tracks":[
      {
         "pos":0,
         "artist_name":"Missy Elliott",
         "track_uri":"spotify:track:0UaMYEvWZi0ZqiDOoHU3YI",
         "artist_uri":"spotify:artist:2wIVse2owClT7go1WT98tk",
         "track_name":"Lose Control (feat. Ciara & Fat Man Scoop)",
         "album_uri":"spotify:album:6vV5UrXcfyQD1wu4Qo2I9K",
         "duration_ms":226863,
         "album_name":"The Cookbook"
      },
      {
         "pos":1,
         "artist_name":"Britney Spears",
         "track_uri":"spotify:track:6I9VzXrHxO9rA9A5euc8Ak",
         "artist_uri":"spotify:artist:26dSoYclwsYLMAKD3tpOr4",
         "track_name":"Toxic",
         "album_uri":"spotify:album:0z7pVBGOD7HCIB7S8eLkLI",
         "duration_ms":198800,
         "album_name":"In The Zone"
      },
      {
         "pos":2,
         "artist_name":"Beyoncé",
         "track_uri":"spotify:track:0WqIKmW4BTrj3eJFmnCKMv",
         "artist_uri":"spotify:artist:6vWDO969PvNqNYHIOW5v0m",
         "track_name":"Crazy In Love",
         "album_uri":"spotify:album:25hVFAxTlDvXbx2X2QkUkE",
         "duration_ms":235933,
         "album_name":"Dangerously In Love (Alben für die Ewigkeit)"
      },...
   ],
   "num_edits":6,
   "duration_ms":11532414,
   "num_artists":37
}
```

## Spotify python api
### Installation
```
pip install spotipy
```
### API Data Schema
- A `Playist`
```json
{
    "collaborative": "bool",
    "description": "str",
    "external_urls": {
        "spotify": "str"
    },
    "href": "str",
    "id": "str",
    "images": [
        {
            "height": "int",
            "url": "str",
            "width": "int"
        }
    ],
    "name": "str",
    "owner": {
        "display_name": "str",
        "external_urls": {
            "spotify": "str"
        },
        "href": "str",
        "id": "str",
        "type": "str",
        "uri": "str"
    },
    "primary_color": "NoneType",
    "public": "bool",
    "snapshot_id": "str",
    "tracks": {
        "href": "str",
        "total": "int"
    },
    "type": "str",
    "uri": "str"
}
```
- A `Track`
```json
{
    "tracks": {
        "href": "str",
        "items": [
            {
                "album": {
                    "album_type": "str",
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "str"
                            },
                            "href": "str",
                            "id": "str",
                            "name": "str",
                            "type": "str",
                            "uri": "str"
                        }
                    ],
                    "available_markets": "List[str]",
                    "external_urls": {
                        "spotify": "str"
                    },
                    "href": "str",
                    "id": "str",
                    "images": [
                        {
                            "height": "int",
                            "url": "str",
                            "width": "int"
                        }
                    ],
                    "name": "str",
                    "release_date": "str",
                    "release_date_precision": "str",
                    "total_tracks": "int",
                    "type": "str",
                    "uri": "str"
                },
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "str"
                        },
                        "href": "str",
                        "id": "str",
                        "name": "str",
                        "type": "str",
                        "uri": "str"
                    }
                ],
                "available_markets": "List[str]",
                "disc_number": "int",
                "duration_ms": "int",
                "explicit": "bool",
                "external_ids": {
                    "isrc": "str"
                },
                "external_urls": {
                    "spotify": "str"
                },
                "href": "str",
                "id": "str",
                "is_local": "bool",
                "name": "str",
                "popularity": "int",
                "preview_url": "str",
                "track_number": "int",
                "type": "str",
                "uri": "str"
            }
        ],
        "limit": "int",
        "next": "str",
        "offset": "int",
        "previous": "NoneType",
        "total": "int"
    }
}
```
- An `Artist`
```json
{
    "external_urls": {
        "spotify": "str"
    },
    "followers": {
        "href": "NoneType",
        "total": "int"
    },
    "genres": "List[str]",
    "href": "str",
    "id": "str",
    "images": [
        {
            "height": "int",
            "url": "str",
            "width": "int"
        }
    ],
    "name": "str",
    "popularity": "int",
    "type": "str",
    "uri": "str"
}
```
- Audio features of a track

## Quickstart

### Data Preparation

```
python src/data_prepare.py --datadir ./data/modeling --mpd_tr ./data/mpd_train --mpd_te ./data/mpd_test
```