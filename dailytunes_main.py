# DailyTunes Main Program
# Sets up web app at localhost:9999
# Written by Srihari Nanniyur

import dailytunes_backend
import spotipy
import spotipy.util as util
import random
import json
from flask import Flask, render_template

track_ids = []
DT_PLAYLIST_ID = "5OArjb97h909aEVGOZnfnt"

scope = 'playlist-modify-public'
token = util.prompt_for_user_token('svn108', scope,
	client_id='d3e4a6a0a90643148eb2802901a03436',
	client_secret='d5331b4fcc454027bb08ca92c543564c',
	redirect_uri='http://localhost:9999/callback/')

if not token:
	raise Exception('Authentication failed. Goodbye.')

spotify = spotipy.Spotify(auth=token)


dailytunes_backend.get_links()
dailytunes_backend.analyze_articles()
analysis_results = dailytunes_backend.find_stats()
print(analysis_results)
print("Total analysis complete.")

# Get a number of tracks from a certain Spotify playlist
def get_playlist_tracks(username, playlist_id, lim):
	global track_ids
	count = 0
	results = spotify.user_playlist_tracks(username, playlist_id)
	tracks = results['items']
	for track in tracks:
		if (count >= lim):
			break
		# Remove everything but track ID
		track_ids.append(track['track']['uri'])
		count += 1


# BEGIN PLAYLISTS
anger_playlists = [
	"37i9dQZF1DWSqBruwoIXkA",
	"37i9dQZF1DWWJOmJ7nRx0C",
	"37i9dQZF1DX2pSTOxoPbx9",
	"37i9dQZF1DX3LDIBRoaCDQ",
	"37i9dQZF1DX4eRPd9frC1m"
]

fear_playlists = [
	"37i9dQZF1DX1s9knjP51Oa",
	"37i9dQZF1DX2iUghHXGIjj",
	"37i9dQZF1DWTtTyjgd08yp",
	"37i9dQZF1DX9LT7r8qPxfa",
	"37i9dQZF1DXarebqD2nAVg"
]

joy_playlists = [
	"37i9dQZF1DXdPec7aLTmlC",
	"37i9dQZF1DWSqmBTGDYngZ",
	"37i9dQZF1DX7KNKjOK0o75",
	"37i9dQZF1DX3rxVfibe1L0",
	"37i9dQZF1DWSkMjlBZAZ07"
]

sadness_playlists = [
	"37i9dQZF1DX3YSRoSdA634",
	"37i9dQZF1DWVV27DiNWxkR",
	"37i9dQZF1DX7gIoKXt0gmx",
	"37i9dQZF1DXarebqD2nAVg",
	"37i9dQZF1DXaiAJKcabR16"

]

# END PLAYLISTS

# BEGIN ACTUAL PLAYLIST ACQUIRING STUFF

i = random.randint(0, 4)

get_playlist_tracks("spotify", anger_playlists[i], int(analysis_results['anger']))
get_playlist_tracks("spotify", fear_playlists[i], int(analysis_results['fear']))
get_playlist_tracks("spotify", joy_playlists[i], int(analysis_results['joy']))
get_playlist_tracks("spotify", sadness_playlists[i], int(analysis_results['sadness']))

# END ACTUAL PLAYLIST ACQUIRING STUFF

# BEGIN SERVER STUFF

def clean_playlist():
	old_results = spotify.user_playlist_tracks("svn108", DT_PLAYLIST_ID)
	old_tracks = old_results['items']
	old_list = []
	for otrack in old_tracks:
		old_list.append(otrack['track']['uri'])
	spotify.user_playlist_remove_all_occurrences_of_tracks("svn108",
								DT_PLAYLIST_ID,
								[element for element in old_list])
clean_playlist()
spotify.user_playlist_add_tracks("svn108", DT_PLAYLIST_ID,
				[element for element in track_ids])

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
	return app.send_static_file('index.html')

app.run(port=9999, debug=False) # Super creative server name there
# END SERVER STUFF
