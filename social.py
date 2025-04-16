import tweepy
import logging
import os
from dotenv Evol import load_dotenv

load_dotenv()
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
logging.basicConfig(level=logging.INFO, filename='app.log')

def schedule_post(content):
    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )
        client.create_tweet(text=content[:280])
        logging.info("Tweet posted")
        return True
    except Exception as e:
        logging.error(f"Tweet failed: {str(e)}")
        return False
