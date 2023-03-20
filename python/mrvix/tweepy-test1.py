# Import the necessary libraries for accessing the Twitter API
import csv
import sys
sys.path.append("/opt/homebrew/lib/python3.10/site-packages")
import tweepy

auth = tweepy.OAuthHandler(7aS2IKCBUrhPquZU1oDHC5Eeb, rIMQwHgotObgOmlucvbQ1Cvsg3lz3W3tIDNB6WpZNRnU43CTjH)
auth.set_access_token(18339688-wzNJeoEwpGE1KqOEWu1qTEKaYgnUuBx0Rw8U2F0YA, UMpnFPAN05PfGynBP7ZKIZuqMqDgZZ5uKbWgLSkmi6r3v)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text