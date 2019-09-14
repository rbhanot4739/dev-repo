import json
from os import environ
import tweepy

HOME = environ.get("HOME")

with open(f"{HOME}/Desktop/twitter.json") as input_file:
    auth_data = json.load(input_file)


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key=auth_data['consumer_key'], consumer_secret=auth_data['consumer_secret'])
    auth.set_access_token(key=auth_data['access_token'], secret=auth_data['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    try:
        api.verify_credentials()
        print("Authentication OK")
        user_messages = api.list_direct_messages()
        for tweet in tweepy.Cursor(api.search, q="@gostackstate", lang="en").items(10):
            print(tweet)
    except Exception as e:
        print(e)