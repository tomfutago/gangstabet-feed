import os
import tweepy
import requests
import time
from dotenv import load_dotenv

load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

def twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    #api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def tweet_image(url, message):
    api = twitter_api()
    media_list = []
    filename = "temp.gif"
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, "wb") as image:
            for chunk in request:
                image.write(chunk)

        response = api.media_upload(filename)

        #uploaded_media = api.media_upload(filename, media_category='TweetImage')
        #while (uploaded_media.processing_info['state'] == 'pending'):
        #    time.sleep(uploaded_media.processing_info['check_after_secs'])
        #    uploaded_media = api.get_media_upload_status(uploaded_media.media_id_string)
        #api.update_status('@' + tweet.author.screen_name + ' ', in_reply_to_status_id=tweet.id_str, media_ids=[uploaded_media.media_id_string])
        #api.update_status(status=message, media_ids=[uploaded_media.media_id_string])

        media_list.append(response.media_id_string)
        #os.remove(filename)
        api.update_status(status=message, media_ids=media_list)
        #api.update_status(status=message)
    else:
        print("Unable to download image")


url = "https://gbet.mypinata.cloud/ipfs/QmNSbSL35cdukZLHY7KSpqR2jvtAcqotnJ2HxKnYHHdSLg/2614.gif"
message = "just test #tweepy"
tweet_image(url, message)
