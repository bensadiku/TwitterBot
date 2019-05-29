#Author: Ben Sadiku. 
#Source: github.com/bensadiku
#Created_At: 5/29/2019.
#License: MIT.

import tweepy
import time

#Import Twitter tokens from the secret_tokens file
from secret_tokens import *

print('Twitter Bot INIT', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

LAST_SEEN_ID_FILE_NAME = 'last_seen_id.txt'

#Used to retreive the last tweet stored.
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

#Used to store the last tweet read.
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(last_seen_id)
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(LAST_SEEN_ID_FILE_NAME)
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(mention.id_str + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id_str
        tweetTxt = mention.full_text.lower()
        store_last_seen_id(last_seen_id, LAST_SEEN_ID_FILE_NAME)
        if '#hello' in tweetTxt:
          
            print('found #hello', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    ' Hi!', mention.id)
     

while True:
    reply_to_tweets()
    time.sleep(15)