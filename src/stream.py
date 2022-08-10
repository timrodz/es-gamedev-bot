import logging
import typing

import tweepy

from src.hashtag_block_list import block_list as hashtag_block_list
from src.word_block_list import block_list as keyword_block_list

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Stream(tweepy.Stream):
    def __init__(
        self, consumer_key, consumer_secret, access_token, access_token_secret, **kwargs
    ):
        super().__init__(
            consumer_key, consumer_secret, access_token, access_token_secret, **kwargs
        )
        # Initialises an instance of the Twitter API in order to have all the functionality available
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret, access_token, access_token_secret
        )

        self.api = tweepy.API(auth)

    def on_status(self, status: tweepy.Tweet):
        # https://docs.tweepy.org/en/stable/v1_models.html#tweepy.models.Status
        logger.info(f"Processing tweet id {status.id}")

        if not self._can_interact_with_tweet(status):
            return

        if not status.retweeted:
            try:
                self.api.retweet(status.id)
                logger.info(
                    f"Retweeted {status.id} with source {status.source}")
            except Exception as e:
                logger.error(f"Error on retweet: {e}", exc_info=True)

    def _can_interact_with_tweet(self, tweet: tweepy.Tweet) -> bool:
        if hasattr(tweet, "possibly_sensitive") and tweet.possibly_sensitive is True:
            logger.info(f"Skipping tweet: {tweet.id} (possibly sensitive)")
            return False

        if hasattr(tweet, "extended_tweet"):
            # Some tweets contain data in the form of an "extended tweet"
            # source: https://docs.tweepy.org/en/stable/extended_tweets.html
            if self._tweet_contains_blocked_hashtags(
                tweet.extended_tweet["entities"]["hashtags"]
            ):
                logger.info(f"Tweet {tweet.id} contains blocked hashtags")
                return False

        if hasattr(tweet, "retweeted_status"):
            logger.warn(f"Skipping tweet: {tweet.id} (retweeted)")
            return False

        if tweet.is_quote_status:
            logger.warn(f"Skipping tweet: {tweet.id} (quoted status)")
            return False

        if self._tweet_contains_blocked_keywords(tweet.text):
            logger.info(f"Tweet {tweet.id} contains blocked keywords")
            return False

        return True

    def _tweet_contains_blocked_keywords(
        self, text: str
    ) -> bool:
        return any(keyword in text.upper() for keyword in keyword_block_list)

    def _tweet_contains_blocked_hashtags(
        self, hashtags: typing.List[typing.Dict[str, str]]
    ) -> bool:
        if not hashtags:
            return False
        _hashtag_list: typing.List[str] = [
            hashtag["text"].upper() for hashtag in hashtags
        ]
        return any(h for h in _hashtag_list if any(bh in h for bh in hashtag_block_list))
