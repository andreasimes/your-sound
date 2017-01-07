# need to import flask 
# run pip install Flask

# moby's dance party is supposed to generate a playlist of songs listed by spotify in the 'soul' genre which are also from 1970-1975
# currently the app can take speech input (play) and return a list of songs displayed using Spotify's play button
# TODO: in moby's dance party, allow user to use their own seach keywords in their voice command 

import os
from flask import Flask, request, render_template, g, redirect, Response, url_for, flash, make_response
import json
import requests
import base64
import urllib
import ast
from unicodedata import normalize

with open('data.json') as json_data_file:
	data = json.load(json_data_file)

# links to config files
CLIENT_ID = data['spotify']['id'] 
CLIENT_SECRET = data['spotify']['secret']


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates') # creates paths for Jinja templates in a templates folder
app = Flask(__name__, template_folder=tmpl_dir)



@app.route("/", methods=['GET','POST']) # initial landing page
def index():
	if request.method == 'POST':
		query = request.form['text']
		
		return redirect(url_for('.results', query=query))
	
	elif request.method == 'GET':
		return render_template('index.html');


@app.route("/results/<query>") # results handling
#@app.route("/moby/<query>")
def results(query):

	# request to spotify API

	# generate token via client credentials auth flow
	var = {'grant_type':'client_credentials'}
	encoded = base64.b64encode(CLIENT_ID+":"+CLIENT_SECRET)
	headers = {'Authorization':'Basic '+encoded}
	r = requests.post('https://accounts.spotify.com/api/token', data=var, headers=headers)
	result = r.text
	token = ast.literal_eval(result)['access_token']
	input = {'q':query,'type':'track', 'limit': '10'}
	r = requests.get('https://api.spotify.com/v1/search', params=input) # request

	
	parsed_json = json.loads(r.text)
	#song = parsed_json['tracks']['items'][0]['name'] # parsing for song
	
	# initialize dictionary to store tracks + info
	songdict = {}
	name = ""
	uri = ""
	trackid = ""

	# iterate over all tracks
	# and access spotify audio features endpoint to return danceability info for each track
	for i in range(0,len(parsed_json['tracks']['items'])):

		# isolate song info
		name = parsed_json['tracks']['items'][i]['name']
		uri = parsed_json['tracks']['items'][i]['uri']
		trackid = parsed_json['tracks']['items'][i]['id']
		
		
		imp={'id':trackid}
		dat = {}
		headers = {'Authorization': 'Bearer ' + token }
		address = "https://api.spotify.com/v1/audio-features/" + trackid
		re = requests.get(address, data=dat, headers=headers)
		new_json = json.loads(re.text)
		danceability = new_json['danceability']
		songdict[name]=[uri, danceability] # update dict track's info

	# separate dictionary for songs with danceability > 0.5 --> more danceable
	display_dict = {}
	for key, value in songdict.iteritems():
		if value[1] > 0.5:
			display_dict[key]=[value[0],value[1]]

	#artist = parsed_json['tracks']['items'][0]['artists'][0]['name'] # parsing for artist 
	#link = parsed_json['tracks']['items'][0]['uri'] # parsing for link

	return render_template('results.html',songdict=display_dict)


@app.route("/moby", methods=['GET']) 
def moby():
	return render_template('moby_dance_party.html') # handling for moby's dance party tab -- initial display


@app.route("/mobyparty/<query>", methods=['POST']) # return results for moby's dance party after voice input
def mobyparty(query):

	#API request for credentials
	var = {'grant_type':'client_credentials'}
	encoded = base64.b64encode(CLIENT_ID+":"+CLIENT_SECRET) # encoding specified by spotify
	headers = {'Authorization':'Basic '+encoded}
	r = requests.post('https://accounts.spotify.com/api/token', data=var, headers=headers)
	result = r.text
	token = ast.literal_eval(result)['access_token']

	#API GET query to Spotify's search endpoint
	query = query + ' year:1970-1972'+' genre:soul'

	input = {'q':query,'type':'track', 'limit': '10'}
	r = requests.get('https://api.spotify.com/v1/search', params=input)
	parsed_json = json.loads(r.text)
	#song = parsed_json['tracks']['items'][0]['name'] # parsing for song
	

	# initialize dictionary to hold track info
	songdict = {}
	name = ""
	uri = ""
	trackid = ""


	# iterate over all tracks returned
	# and access audio features API to get info for danceability
	# and store their info in dictionary
	for i in range(0,len(parsed_json['tracks']['items'])):

		name = parsed_json['tracks']['items'][i]['name']
		uri = parsed_json['tracks']['items'][i]['uri']
		trackid = parsed_json['tracks']['items'][i]['id']
		imp={'id':trackid}
		dat = {}
		headers = {'Authorization': 'Bearer ' + token }
		address = "https://api.spotify.com/v1/audio-features/" + trackid
		re = requests.get(address, data=dat, headers=headers)
		new_json = json.loads(re.text)
		danceability = new_json['danceability']
		songdict[name]=[uri, danceability] #update dict track's info


	# handling to separate tracks with danceability score > 0.5 --> more danceable
	display_dict = {}
	for key, value in songdict.iteritems():
		if value[1] > 0.5:
			display_dict[key]=[value[0],value[1]]
	

	
	return render_template('moby.html',songdict=display_dict)

if __name__ == "__main__":
	app.run()
