# Spotify-Recommendation

## Spotify Million Playlist Dataset Preparation
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

## Spotify python api
### Installation
```
pip install spotipy
```
### Data Schema
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
