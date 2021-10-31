import os
import tweepy
from dotenv import load_dotenv

load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth_url = auth.get_authorization_url()
print('Visit this URL and authorise the app to use your Twitter account: ' + auth_url)
verifier = input('Type in the generated PIN: ').strip()
auth.get_access_token(verifier)

# Print out the information for the user
print("consumer_key        = '%s'" % consumer_key)
print("consumer_secret     = '%s'" % consumer_secret)
print("access_token        = '%s'" % auth.access_token)
print("access_token_secret = '%s'" % auth.access_token_secret)
