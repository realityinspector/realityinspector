# Import the necessary libraries for accessing the Twitter API
import sys
sys.path.append("/opt/homebrew/lib/python3.10/site-packages")
import tweepy
import csv

# Enter your Twitter API keys here
consumer_key = "7aS2IKCBUrhPquZU1oDHC5Eeb"
consumer_secret = "rIMQwHgotObgOmlucvbQ1Cvsg3lz3W3tIDNB6WpZNRnU43CTjH"
access_token = "18339688-wzNJeoEwpGE1KqOEWu1qTEKaYgnUuBx0Rw8U2F0YA"
access_token_secret = "UMpnFPAN05PfGynBP7ZKIZuqMqDgZZ5uKbWgLSkmi6r3v"

# Authenticate with the Twitter API using your keys and the OAuth 2.0 flow
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Set up a CSV file to store the search results
csv_file = open('twitter_search_results.csv', 'w')
csv_writer = csv.writer(csv_file)

# Define the search terms and the number of tweets to retrieve
search_terms = ["mr. vix", "mrvix", "mad genius"]
num_tweets = 100

# Search Twitter for each of the search terms and store the results
for term in search_terms:
  tweets = tweepy.Cursor(api.search, q=term, tweet_mode='extended').items(num_tweets)

  # Loop through the search results and write them to the CSV file
  for tweet in tweets:
    url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
    text = tweet.full_text
    author_handle = tweet.user.screen_name
    author_name = tweet.user.name
    post_author = tweet.retweeted_status.user.name if hasattr(
      tweet, "retweeted_status") else None

    csv_writer.writerow([url, text, author_handle, author_name, post_author])

# Close the CSV file when finished
csv_file.close()
