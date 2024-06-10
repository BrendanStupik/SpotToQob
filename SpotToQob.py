import csv
import subprocess
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import configparser
import sys
import re
import argparse
import os

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def create_config(config_file):
    config = configparser.ConfigParser()
    use_api = input("Do you want to use the Spotify API? (yes/no) (Note: API keys are required to download large playlists): ").lower()
    if use_api == "yes" or use_api == "y":
        client_id = input("Enter your Spotify Client ID: ")
        client_secret = input("Enter your Spotify Client Secret: ")
    elif use_api == "no" or use_api == "n":
        client_id = 'xxxxxxxx'
        client_secret = 'xxxxxxxx'
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        sys.exit(1)

    config['SpotifyAPI'] = {
        'ClientID': client_id,
        'ClientSecret': client_secret
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def clean_album_name(album_name):
    keywords = ['remaster', 'anniversary', 'deluxe', 'studio master', 'expanded']
    for keyword in keywords:
        album_name = re.sub(rf'\(.*?{keyword}.*?\)', '', album_name, flags=re.IGNORECASE)
    return album_name.strip()

def clean_track_name(track_name):
    track_name = re.sub(r'\([^)]*\)', '', track_name)
    track_name = re.sub(r'\[[^\]]*\]', '', track_name)
    track_name = re.sub(r' - \d{4} remaster.*$', '', track_name)
    track_name = re.sub(r' - [^\-]*$', '', track_name)
    return track_name.strip()

def get_playlist_tracks(playlist_url, config):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=config.get('SpotifyAPI', 'ClientID'),
        client_secret=config.get('SpotifyAPI', 'ClientSecret')
    )
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    playlist_id = playlist_url.split('/')[-1].split('?')[0]

    try:
        playlist = sp.playlist(playlist_id)
        playlist_name = playlist['name']
    except Exception as e:
        print(f"Error fetching playlist details: {e}")
        return []

    try:
        all_tracks = []
        offset = 0
        while True:
            tracks = sp.playlist_tracks(playlist_id, offset=offset)
            all_tracks.extend(tracks['items'])
            offset += len(tracks['items'])
            if not tracks['next']:
                break
    except Exception as e:
        print(f"Error fetching playlist tracks: {e}")
        return []

    playlist_details = []
    for item in all_tracks:
        try:
            track = item['track']
            if track:
                track_details = {
                    'Playlist Name': playlist_name,
                    'Track Name': clean_track_name(track['name']),
                    'Artist Name(s)': ', '.join(artist['name'] for artist in track['artists']),
                    'Album': clean_album_name(track['album']['name'])
                }
                playlist_details.append(track_details)
        except Exception as e:
            print(f"Error processing track details: {e}")

    return playlist_details

def search_qobuz_dl(artist, album=None, song=None):
    if song:
        query = f'qobuz-dl lucky -t track "{artist} - {song}"'
    else:
        query = f'qobuz-dl lucky "{artist} - {album}"'
    subprocess.run(query, shell=True)

def main():
    parser = argparse.ArgumentParser(description="Process Spotify playlists and search qobuz-dl.")
    parser.add_argument("input", nargs='?', help="Spotify playlist URL or CSV file")
    parser.add_argument("--songs", action="store_true", help="Search for songs")
    parser.add_argument("--albums", action="store_true", help="Search for albums")
    parser.add_argument("--config", default="config.ini", help="Location of the config file")
    parser.add_argument("--reconfigure", action="store_true", help="Recreate the config file")

    args = parser.parse_args()

    if args.reconfigure:
        create_config(args.config)
        sys.exit(0)

    if not args.songs and not args.albums:
        print("You must specify either --songs or --albums")
        sys.exit(1)

    config_file = args.config
    if not os.path.exists(config_file):
        create_new_config = input("No config found. Create one? (yes/no): ")
        if create_new_config.lower() == "yes" or create_new_config.lower() == "y":
            create_config(config_file)
        else:
            print("Exiting program. Please create a config or specify its location (using --config).")
            sys.exit(0)

    config = load_config(config_file)

    if args.input and args.input.endswith('.csv'):
        with open(args.input, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            all_playlist_tracks = []
            for row in reader:
                track_details = {
                    'Track Name': clean_track_name(row['Track Name']),
                    'Artist Name(s)': row['Artist Name(s)'],
                    'Album': clean_album_name(row['Album Name'])
                }
                all_playlist_tracks.append(track_details)

    elif args.input:
        playlist_tracks = get_playlist_tracks(args.input, config)
        all_playlist_tracks = playlist_tracks
    else:
        all_playlist_tracks = []

    csv_file_path = 'playlist_tracks.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Playlist Name', 'Track Name', 'Artist Name(s)', 'Album']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_playlist_tracks)

    for track in all_playlist_tracks:
        if args.songs:
            search_qobuz_dl(track['Artist Name(s)'], song=track['Track Name'])
        elif args.albums:
            search_qobuz_dl(track['Artist Name(s)'], album=track['Album'])

    os.remove(csv_file_path)

if __name__ == "__main__":
    main()
