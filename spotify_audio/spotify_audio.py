import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os
import pandas as pd

USERNAME = "ianforme"
CLIENT_ID = "0425d4bf14324cae940a69ae12389342"
CLIENT_SECRET = "6b73c8ddff384a239095704089f04a03"
SCOPE = "user-library-read"
REDIRECT_URI = "https://beta.developer.spotify.com/dashboard/applications/0425d4bf14324cae940a69ae12389342"

billboard_by_decades = {
	"00s" : "0UpEURMf6HDxPqTxb0ywMh",
	"90s" : "0GpHnLbbbrvtqdW5BTVrq8",
	"80s" : "2pe5ZmQYNQXB3lW5BC4G6b",
	"70s" : "6c4uHQAWjbWEcJkiKXbtLB",
	"60s" : "6T6ALn3CAxHTFy0pVZ56wC"
}
try:
    token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
except (AttributeError):
    os.remove(".cache-%s"%USERNAME)
    token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

sp = spotipy.Spotify(auth=token)

for decade in billboard_by_decades.keys():
	tracks = sp.user_playlist_tracks("1242049382", playlist_id=billboard_by_decades[decade])
	features = []
	for i, item in enumerate(tracks['items']):
		track = item['track']

		album = track['album']['name']
		artist = track['artists'][0]['name']
		name = track['name']
		popularity = track['popularity']

		track_features = sp.audio_features(str(track['uri']))
		
		energy = track_features[0]['energy']
		liveness = track_features[0]['liveness']
		tempo = track_features[0]['tempo']
		speechiness = track_features[0]['speechiness']
		acousticness = track_features[0]['acousticness']
		instrumentalness = track_features[0]['instrumentalness']
		time_signature = track_features[0]['time_signature']
		danceability = track_features[0]['danceability']
		key = track_features[0]['key']
		duration_ms = track_features[0]['duration_ms']
		loudness = track_features[0]['loudness']
		valence = track_features[0]['valence']
		mode = track_features[0]['mode']

		features.append([i, name, album, artist, energy, liveness, tempo, speechiness, acousticness, instrumentalness, time_signature,\
		danceability, key, duration_ms, loudness, valence, mode, popularity])

	df = pd.DataFrame(features, columns=["id", "name", "album", "artist", "energy", "liveness", "tempo", "speechiness", "acousticness",\
			"instrumentalness", "time_signature", "danceability", "key", "duration_ms", "loudness", "valence", "mode", "popularity"])
	df.to_csv("%s_audio_features.csv"%decade, encoding="utf-8")

