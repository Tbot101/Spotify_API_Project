import json
from pprint import pprint
import requests
import password
import sys


class lastFmSpotify:
    def __init__(self):
        self.token = password.spotify_token()
        self.api_key = password.last_fm_api_key()
        self.user_id = password.spotify_user_id()
        self.spotify_headers = {"Content-Type": "application/json",
                                "Authorization": f"Bearer {self.token}"}
        self.playlist_id = ''
        self.song_info = {}
        self.uri = []

    def fetch_songs_from_lastfm(self):
        url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&format=json"
        params = {"limit": 20, "api_key": self.api_key}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            self.exceptionalExceptions(response.status_code, response.text)
        res = response.json()
        song_info = dict()
        for item in res['tracks']['track']:
            name = item['name'].title()
            artist = item['artist']['name'].title()
            song_info[name] = artist
        return song_info

    def get_uri_from_spotify(self, song_info):
        uri_list = []
        for name, artist in song_info.items():
            url = f"https://api.spotify.com/v1/search?q=track%3A{name}+artist%3A{artist}&type=track&limit=5"
            response = requests.get(url, headers=self.spotify_headers)
            res = response.json()
            output_uri = res['tracks']['items']
            uri = output_uri[0]['uri']
            uri_list.append(uri)
        return uri_list

    def create_spotify_playlist(self, name, desc):
        data = {
            "name": name,
            "description": desc,
            "public": False
        }
        data = json.dumps(data)
        url = f'https://api.spotify.com/v1/users/{self.user_id}/playlists'
        response = requests.post(url, data, headers=self.spotify_headers)
        if response.status_code == 201:
            print("Successfully created Spotify Playlist")
            id_number = response.json()
            return id_number["id"]
        else:
            self.exceptionalExceptions(response.status_code, response.text)
        print("Created playlist")

    def add_songs_to_playlist(self, uri_list, playlist_id):
        uris = json.dumps(uri_list)
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.post(
            url, data=uris, headers=self.spotify_headers)
        if response.status_code == 201:
            print("Songs added successfully")
        else:
            self.exceptionalExceptions(response.status_code, response.text)

    def list_songs_in_playlist(self, playlist_id):
        self.playlist_id = "2m33AWbDAIO4aQP119JEhe"
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.get(url, headers=self.spotify_headers)
        if response.status_code != 200:
            self.exceptionalExceptions(response.status_code, response.text)
        else:
            res = response.json()
            songs = []
            for item in res['items']:
                songs.append(item['track']['name'])
        return songs

    def exceptionalExceptions(self, status_code, err):
        print("Exception occurred with status_code: ", status_code)
        print("Error: ", err)
        sys.exit(0)
