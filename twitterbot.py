import tweepy
import spotipy
import spotipy.util as util
import sys
import time
import requests
import config

spotify_client_id= config.spotify_client_id
spotify_client_secret= config.spotify_client_secret
spotify_redirect_uri = config.spotify_redirect_uri
spotify_username = config.spotify_username
scopes = 'user-library-read user-read-playback-state'
twitter_consumer_key = config.consumer_key
twitter_consumer_secret_key = config.secret_consumer_key
twitter_access_token = config.access_token
twitter_aaccess_token_secret = config.access_token_secret

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret_key)
auth.set_access_token(twitter_access_token, twitter_aaccess_token_secret)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

print('this is my twitter bot', flush=True)

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def getToken():
    token = util.prompt_for_user_token(spotify_username,scopes,client_id=spotify_client_id,client_secret=spotify_client_secret,redirect_uri=spotify_redirect_uri)
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
        #print(current_track["track_name"])
        return current_track["track_name"]
    else:
        #print("user is not playing any tracks")
        return "user is not playing any tracks"

def reply_to_tweets():
    
    print('retrieving and replying to tweets...', flush=True)
    song = getMyCurrentPlayback()
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '!song' in mention.full_text.lower():
            print('found #helloworld!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    ' Nikhil is listening to: ' + song, mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)




