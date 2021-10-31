import os
import tweepy
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


#Reformat the keys and encode them
key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
#Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
print(auth_resp.status_code)
access_token = auth_resp.json()['access_token']
#print(access_token)

file = open('C:/Temp/th.jpg', 'rb')
data = file.read()
resource_url = 'https://upload.twitter.com/1.1/media/upload.json'
upload_image = {
    'media':data,
    'media_category':'tweet_image'}
    
image_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}

media_id = requests.post(resource_url, headers=image_headers, params=upload_image)
print(media_id.status_code)

"""
tweet_meta={ "media_id": media_id,
  "alt_text": {
    "text":"tlogo" 
  }}
metadata_url = 'https://upload.twitter.com/1.1/media/metadata/create.json'    
metadata_resp = requests.post(metadata_url, params=tweet_meta, headers=auth_data)
print(metadata_resp.status_code)

#tweet = {'status': 'just test #tweepy', 'media_ids': media_id}
tweet = {'status': 'just test #tweepy'}
post_url = 'https://api.twitter.com/1.1/statuses/update.json'    
post_resp = requests.post(post_url, params=tweet, headers=image_headers)
print(post_resp.status_code)
"""

#try:
#    api.verify_credentials()
#    print("Authentication OK")
#    api.update_status("just test.. #tweepy")
#except:
#    print("Error during authentication")
