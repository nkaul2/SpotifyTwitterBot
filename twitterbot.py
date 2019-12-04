import tweepy
import spotipy
import spotipy.util as util
import sys
import requests
import config

client_id= config.client_id
client_secret= config.client_secret
redirect_uri = config.redirect_uri
username = config.username
scopes = 'user-library-read user-read-playback-state'

def getToken():
    token = util.prompt_for_user_token(username,scopes,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    return token

def getMyCurrentPlayback():
    oauth_token = getToken()
    url = "https://api.spotify.com/v1/me/player"
    data = requests.get(url, headers={"Authorization": 'Bearer ' + oauth_token})
    if data.status_code == 200: 
        data = data.json()
        track_id = data['item']['id']
        track_name = data['item']['name']
        track_uri = data['item']['uri']
        track_external_url = data['item']['external_urls']['spotify']
        artists_name = ""
        for i in data['item']['artists']: 
            artists_name += (i['name'] + ", ")

        current_track  = { 
            "track_id" : track_id, 
            "track_name": track_name, 
            "track_uri": track_uri, 
            "track_external_url": track_external_url, 
            "artists_name": artists_name[:-2]
        }
        print(current_track["track_name"])
    else:
        print("user is not playing any tracks")

if __name__ == '__main__':
    getMyCurrentPlayback()


