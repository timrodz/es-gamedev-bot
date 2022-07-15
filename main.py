import logging
import os
import typing

import tweepy
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


"""
We want to block any tweet that contains a remote hashtag match with any of our items inside the blocklist
If our tweet contains the hashtag "NFT", we 1-1 match it against our item "NFT"
If it has "NFT1", it also needs to be blocked because it matches "NFT"
If it only contains an "N", we do not watch to block it because that doesn't match "NFT"
"""
hashtag_block_list: typing.List[str] = ["NFT"]


class RetweetStreamListener(tweepy.Stream):
    def on_status(self, status):
        logger.info(f"Processing tweet id {status.id}")

        if not self.can_interact_with_tweet(status):
            return

        if not status.retweeted:
            try:
                status.retweet()
                logger.info(f"Retweeted: {status.id}")
            except Exception as e:
                logger.error(f"Error on retweet: {e}", exc_info=True)

    def tweet_contains_blocked_hashtag(
        self, hashtags: typing.List[typing.Dict[str, str]]
    ) -> bool:
        _hashtag_list: typing.List[str] = [
            hashtag["text"].upper() for hashtag in hashtags
        ]
        return any(
            h for h in _hashtag_list if any(bh in h for bh in hashtag_block_list)
        )

    def can_interact_with_tweet(self, tweet) -> bool:
        # Ignore tweet if it's either mine or a reply
        if tweet.user.id == self.me.id:
            logger.info(f"Skipping tweet: {tweet.id} (mine or reply to me)")
            return False

        try:
            if tweet.possibly_sensitive:
                logger.info(f"Skipping tweet: {tweet.id} (possibly sensitive)")
                return False
        except:
            pass

        # Filter out bad hashtags
        try:
            # Some tweets contain data in the form of an "extended tweet"
            # source: https://docs.tweepy.org/en/stable/extended_tweets.html
            et = tweet.extended_tweet
            if self.tweet_contains_blocked_hashtag(et["entities"]["hashtags"]):
                return False
        except:
            # Tweet is compatibility mode, extract data in another way
            if self.tweet_contains_blocked_hashtag(tweet.entities["hashtags"]):
                return False

        # Ignore tweet if it's a quote retweet
        if tweet.is_quote_status:
            logger.info(f"Skipping tweet: {tweet.id} (quoted status)")
            return False

        try:
            # Ignore tweet if it's a retweet
            retweet = tweet.retweeted_status
            logger.info(f"Skipping tweet: {retweet.id} (retweeted)")
            return False
        except Exception:
            return True


if __name__ == "__main__":
    keywords = [
        "#gamedev",
        "#indiedev",
        "#madewithunity",
        "#UE4",
        "#gamedev español",
    ]

    languages = ["en"]

    stream_listener = RetweetStreamListener(
        os.getenv("API_KEY"),
        os.getenv("API_SECRET_KEY"),
        os.getenv("ACCESS_TOKEN"),
        os.getenv("ACCESS_TOKEN_SECRET"),
    )
    stream_listener.filter(
        track=keywords, languages=languages, filter_level="low")
