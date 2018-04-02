import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import traceback

CLIENT_ID = 'a8f90fb217ea429688a346d70bd41f88'
CLIENT_SECRET = '49fdbe3b1e714020b8bcb292482a572c'

class SpotifyExtractor(object):
	def __init__(self,client_id = CLIENT_ID, client_secret = CLIENT_SECRET):
		self.client_id = client_id
		self.client_secret = client_secret
		self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id,client_secret = self.client_secret)
		self.sp = spotipy.Spotify(client_credentials_manager = self.client_credentials_manager)
		print("Spotify Extractor Initiated!")
	def get_artist_uri(self,artist_name):
		try:
			results = self.sp.search(artist_name,limit = 1, 
				type='artist',)
			artist_uri = results['artists']['items'][0]['uri']
			return artist_uri
		except:
			print ("Error!!!!... No matching artist...")
	def get_albums(self,artist_name):
		try:
			artist_uri = self.get_artist_uri(artist_name)
			results = self.sp.artist_albums(artist_uri,limit = 20,album_type = 'album')
			albums = results['items']
			albums_dict = []
			for album in albums:
					record = {}
					record['name'] = album['name']	
					record['album_uri'] = album['uri']
					record['release_date'] = album['release_date']
					albums_dict.append(record)
			return albums_dict
		except Exception as e:
			print(e)
			print("No album for artist_uri: " + artist_uri)
	def get_all_songs(self,artist_name):
		output = []
		try:
			albums = self.get_albums(artist_name)
			for album in albums:
				songs = self.sp.album_tracks(album['album_uri'])
				for i in range(len(songs['items'])):
					song = songs['items'][i]
					record = {**album,**song}
					output.append(record)

			df = pd.DataFrame.from_dict(output)
			uris = df['uri'].tolist()
			l = len(uris)
			features = pd.DataFrame()
			for index in range(0,l,50):
				tmp = uris[index:min(index + 50, l)]
				feature = pd.DataFrame.from_dict(self.sp.audio_features(tmp))
				popularity = pd.DataFrame.from_dict(self.sp.tracks(tmp)['tracks'])
				popularity = popularity[['id','popularity']]
				feature = feature.merge(popularity, on='id')
				features = features.append(feature,ignore_index = True) 
			df = df.merge(features,on=['uri','id'])
			df.drop(['artists','type_x','type_y','external_urls','track_href'],axis = 1,inplace=True)
			df['artist'] = artist_name

			df = df.reindex_axis(sorted(df.columns), axis=1)
			df.to_csv(artist_name + '_all_songs.csv')
			print('All songs retrieved!')
		except Exception as e:
			traceback.print_exc()
			print("Error in getting all songs!!!...")




if __name__ == '__main__':
	extractor = SpotifyExtractor()
	extractor.get_all_songs('Taylor Swift')
	