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