import logging
import typing

import tweepy

from src import hashtag_block_list

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

    def on_status(self, status):
        # https://docs.tweepy.org/en/stable/v1_models.html#tweepy.models.Status
        logger.info(f"Processing tweet id {status.id}")

        if not self._can_interact_with_tweet(status):
            return

        if not status.retweeted:
            try:
                self.api.retweet(id)
                logger.info(f"Retweeted: {status.id}")
            except Exception as e:
                logger.error(f"Error on retweet: {e}", exc_info=True)

    def _can_interact_with_tweet(self, tweet: tweepy.Tweet) -> bool:
        if tweet.possibly_sensitive is not None and tweet.possibly_sensitive is True:
            logger.info(f"Skipping tweet: {tweet.id} (possibly sensitive)")
            return False

        try:
            # Some tweets contain data in the form of an "extended tweet"
            # source: https://docs.tweepy.org/en/stable/extended_tweets.html
            et = tweet.extended_tweet
            if self._tweet_contains_blocked_hashtag(et["entities"]["hashtags"]):
                return False
        except:
            # Tweet is compatibility mode, extract data in another way
            if self._tweet_contains_blocked_hashtag(tweet.entities["hashtags"]):
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

    def _tweet_contains_blocked_hashtag(
        self, hashtags: typing.List[typing.Dict[str, str]]
    ) -> bool:
        _hashtag_list: typing.List[str] = [
            hashtag["text"].upper() for hashtag in hashtags
        ]
        return any(
            h for h in _hashtag_list if any(bh in h for bh in hashtag_block_list)
        )
