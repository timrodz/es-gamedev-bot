import os

import tweepy
from dotenv import load_dotenv
from structlog import get_logger

from src.api import get_api

load_dotenv()
log = get_logger()


def should_save_tweet(text, strings_to_save):
    for string in strings_to_save:
        if text.find(string) > -1:
            log.info("Found", str=string, text=text)
            return True

    return False


if __name__ == "__main__":
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_SECRET_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # Don't delete a tweet if it has more than this number of favorites
    max_favs = 4

    # Don't delete a tweet if it has more than this number of retweets
    max_rts = 4

    deletion_count = 0
    ignored_count = 0

    api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)

    log.info("Retrieving timeline tweets")
    for tweet in tweepy.Cursor(api.user_timeline).items():
        log.info("Processing tweet", id=tweet.id)
        # Where tweets are not in save list and older than cutoff date
        if (
            not should_save_tweet(text=tweet.text, strings_to_save=[])
            and tweet.favorite_count < max_favs
            and tweet.retweet_count < max_rts
        ):
            log.info("Delete", id=tweet.id, created_at=tweet.created_at)
            api.destroy_status(tweet.id)
            deletion_count += 1
        else:
            ignored_count += 1
