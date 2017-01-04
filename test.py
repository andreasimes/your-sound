# need to import flask 
# run pip install Flask

import os
#import requests
#import json
from flask import Flask, request, render_template, g, redirect, Response, url_for, flash, make_response
import json
#from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib
import ast
from unicodedata import normalize


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)



@app.route("/", methods=['GET','POST'])
def index():
	if request.method == 'POST':
		print('hi')
		query = request.form['text']
		print(query)
		
		return redirect(url_for('.results', query=query))
		#return redirect(url_for('.moby', query=query))
		#return redirect(url_for('.results'))
	
	elif request.method == 'GET':
		return render_template('index.html');



CLIENT_ID = "78f7c13de8b44da2b92b70e2235cb316"
CLIENT_SECRET = "4e64b9b4da8d4276ac86e1de7c994f3a"

@app.route("/results/<query>")
#@app.route("/moby/<query>")
def results(query):
	var = {'grant_type':'client_credentials'}
	#req = make_response(render_template('https://accounts.spotify.com/api/token', params=var))
	encoded = base64.b64encode(CLIENT_ID+":"+CLIENT_SECRET)
	#resp = flask.Response("https://accounts.spotify.com/api/token")
	#req.headers['Authorization']=["Basic " + encoded]
	headers = {'Authorization':'Basic '+encoded}
	
	#print("78f7c13de8b44da2b92b70e2235cb316:4e64b9b4da8d4276ac86e1de7c994f3a".encode("utf-8"))
	#print(headers)
	#print(json.dumps(var))
	r = requests.post('https://accounts.spotify.com/api/token', data=var, headers=headers)
	##print(r.headers)
	#return r.text, r.raise_for_status()
	result = r.text

	token = ast.literal_eval(result)['access_token']

	input = {'q':query,'type':'track', 'limit': '10'}
	r = requests.get('https://api.spotify.com/v1/search', params=input)

	#url = 'https://api.spotify.com/v1/audio-features/'
	

	#print(r.encode('ascii','ignore'))
	parsed_json = json.loads(r.text)
	#song = parsed_json['tracks']['items'][0]['name']
	songdict = {}
	#print(type(len(parsed_json['tracks']['items'])))
	name = ""
	uri = ""
	trackid = ""
	for i in range(0,len(parsed_json['tracks']['items'])):
		name = parsed_json['tracks']['items'][i]['name']
		uri = parsed_json['tracks']['items'][i]['uri']
		trackid = parsed_json['tracks']['items'][i]['id']
		
		#first_artist_genres = parsed_json['tracks']['items'][0]['artists'][0]['genres']
		#print(name)
		#print(uri)
		#print(trackid)
		imp={'id':trackid}
		dat = {}
		headers = {'Authorization': 'Bearer ' + token }
		address = "https://api.spotify.com/v1/audio-features/" + trackid
		re = requests.get(address, data=dat, headers=headers)
		new_json = json.loads(re.text)
		danceability = new_json['danceability']

		songdict[name]=[uri, danceability] #update dict track's info

	display_dict = {}
	for key, value in songdict.iteritems():
		if value[1] > 0.5:
			display_dict[key]=[value[0],value[1]]
	#print(display_dict)

	#artist = parsed_json['tracks']['items'][0]['artists'][0]['name']
	#link = parsed_json['tracks']['items'][0]['uri']
	#return render_template('index.html',name=name)
	#return render_template('results.html',song=song, artist=artist, link=link, songdict=songdict)
	return render_template('results.html',songdict=display_dict)
#def moby(query):


@app.route("/moby", methods=['GET','POST'])
def moby():
	if request.method == 'GET':
		return render_template('moby_dance_party.html')
	else:
		var = {'grant_type':'client_credentials'}
		#req = make_response(render_template('https://accounts.spotify.com/api/token', params=var))
		encoded = base64.b64encode(CLIENT_ID+":"+CLIENT_SECRET)
		#resp = flask.Response("https://accounts.spotify.com/api/token")
		#req.headers['Authorization']=["Basic " + encoded]
		headers = {'Authorization':'Basic '+encoded}
		
		#print("78f7c13de8b44da2b92b70e2235cb316:4e64b9b4da8d4276ac86e1de7c994f3a".encode("utf-8"))
		#print(headers)
		#print(json.dumps(var))
		r = requests.post('https://accounts.spotify.com/api/token', data=var, headers=headers)
		##print(r.headers)
		#return r.text, r.raise_for_status()
		result = r.text

		token = ast.literal_eval(result)['access_token']

		query = 'love' + ' year:1970-1972'+' genre:soul'
		input = {'q':query,'type':'track', 'limit': '10'}
		r = requests.get('https://api.spotify.com/v1/search', params=input)

		#url = 'https://api.spotify.com/v1/audio-features/'
		

		#print(r.encode('ascii','ignore'))
		parsed_json = json.loads(r.text)
		#song = parsed_json['tracks']['items'][0]['name']
		songdict = {}
		#print(type(len(parsed_json['tracks']['items'])))
		name = ""
		uri = ""
		trackid = ""
		for i in range(0,len(parsed_json['tracks']['items'])):
			name = parsed_json['tracks']['items'][i]['name']
			uri = parsed_json['tracks']['items'][i]['uri']
			trackid = parsed_json['tracks']['items'][i]['id']
			
			#first_artist_genres = parsed_json['tracks']['items'][0]['artists'][0]['genres']
			#print(name)
			#print(uri)
			#print(trackid)
			imp={'id':trackid}
			dat = {}
			headers = {'Authorization': 'Bearer ' + token }
			address = "https://api.spotify.com/v1/audio-features/" + trackid
			re = requests.get(address, data=dat, headers=headers)
			new_json = json.loads(re.text)
			danceability = new_json['danceability']

			songdict[name]=[uri, danceability] #update dict track's info

		display_dict = {}
		for key, value in songdict.iteritems():
			if value[1] > 0.5:
				display_dict[key]=[value[0],value[1]]
		#print(display_dict)

		#artist = parsed_json['tracks']['items'][0]['artists'][0]['name']
		#link = parsed_json['tracks']['items'][0]['uri']
		#return render_template('index.html',name=name)
		#return render_template('results.html',song=song, artist=artist, link=link, songdict=songdict)
		return render_template('moby.html',songdict=display_dict)

if __name__ == "__main__":
	app.run()
