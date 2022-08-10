import typing

from structlog import get_logger
import tweepy

from src.hashtag_block_list import block_list as hashtag_block_list
from src.keyword_block_list import block_list as keyword_block_list

log = get_logger()


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
        log.info(
            "Processing tweet",
            id=status.id,
            created_at=status.created_at,
            entities=status.entities if hasattr(status, "entities") else None,
        )

        if not self._can_interact_with_tweet(status):
            return

        if not status.retweeted:
            try:
                log.info("Retweet", id=status.id)
                self.api.retweet(status.id)
            except Exception as e:
                log.error("Error on retweet", exc_info=e)

    def _can_interact_with_tweet(self, tweet: tweepy.Tweet) -> bool:
        if hasattr(tweet, "reply_settings") and "everyone" not in tweet.reply_settings:
            log.info("Ignore tweet", reason="user does not allow 'everyone' to reply")
            return False

        if hasattr(tweet, "possibly_sensitive") and tweet.possibly_sensitive is True:
            log.info("Ignore tweet", reason="possibly sensitive")
            return False

        if hasattr(tweet, "entities"):
            # Some tweets contain data in the form of an "extended tweet"
            # source: https://docs.tweepy.org/en/stable/extended_tweets.html
            if self._tweet_urls_contain_blocked_keywords(
                tweet.id, tweet.entities["urls"]
            ):
                log.info("Ignore tweet", reason="URLs contain blocked keywords")
                return False

            if self._tweet_contains_blocked_hashtags(tweet.entities["hashtags"]):
                log.info("Ignore tweet", reason="contains blocked hashtags")
                return False

        if hasattr(tweet, "retweeted_status"):
            log.warn("Ignore tweet", reason="retweeted")
            return False

        if tweet.is_quote_status:
            log.warn("Ignore tweet", reason="quoted status")
            return False

        if self._tweet_contains_blocked_keywords(tweet.text):
            log.info("Ignore tweet", reason="contains blocked keywords")
            return False

        return True

    def _tweet_contains_blocked_keywords(self, text: str) -> bool:
        return any(keyword in text.upper() for keyword in keyword_block_list)

    def _tweet_urls_contain_blocked_keywords(
        self, id: str, urls: typing.List[typing.Dict[str, str]]
    ) -> bool:
        if not urls:
            return False

        _url_list: typing.List[str] = [url["expanded_url"].upper() for url in urls]
        log.debug("Check for blocked URLs", urls=_url_list)

        # Make a temporary blocklist that checks to see if the same ID of the tweet is in the URL
        # This is an obfuscation other bots use to hide their links. Clever, but not that clever ;)
        temp_block_list: typing.List[str] = keyword_block_list + [id]

        return any(
            url for url in _url_list if any(key in url for key in temp_block_list)
        )

    def _tweet_contains_blocked_hashtags(
        self, hashtags: typing.List[typing.Dict[str, str]]
    ) -> bool:
        if not hashtags:
            return False

        _hashtag_list: typing.List[str] = [
            hashtag["text"].upper() for hashtag in hashtags
        ]
        log.debug("Check for blocked hashtags", hashtags=_hashtag_list)
        return any(
            hashtag
            for hashtag in _hashtag_list
            if any(key in hashtag for key in hashtag_block_list)
        )
