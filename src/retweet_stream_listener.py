import logging

from config import Config
from src.stream_listener import StreamListener
from src.twitter_api import get_api
import hashtag_filter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class RetweetStreamListener(StreamListener):
    def can_interact_with_tweet(self, tweet) -> bool:
        # Ignore tweet if it's either mine or a reply
        if tweet.user.id == self.me.id:
            logger.info(f'Skipping tweet: {tweet.id} (mine or reply to me)')
            return False
        
        try:
            if tweet.possibly_sensitive:
                logger.info(f'Skipping tweet: {tweet.id} (possibly sensitive)')
                return False
        except:
            pass

        # Filter out bad hashtags
        try:
            # Some tweets contain data in the form of an "extended tweet"
            # source: https://docs.tweepy.org/en/stable/extended_tweets.html
            et = tweet.extended_tweet
            if hashtag_filter.tweet_contains_blocked_hashtag(et["entities"]["hashtags"]):
                return False
        except:
            # Tweet is compatibility mode, extract data in another way
            if hashtag_filter.tweet_contains_blocked_hashtag(tweet.entities["hashtags"]):
                return False

        # Ignore tweet if it's a quote retweet
        if tweet.is_quote_status:
            logger.info(f'Skipping tweet: {tweet.id} (quoted status)')
            return False
        
        try:
            # Ignore tweet if it's a retweet
            retweet = tweet.retweeted_status
            logger.info(f'Skipping tweet: {retweet.id} (retweeted)')
            return False
        except Exception:
            return True
            
    def on_status(self, tweet):
        logger.info(f'Processing tweet id {tweet.id}')
        
        if not self.can_interact_with_tweet(tweet):
            return

        if not tweet.retweeted:
            try:
                tweet.retweet()
                logger.info(f'Retweeted: {tweet.id}')
            except Exception as e:
                logger.error(f'Error on retweet: {e}', exc_info=True)


if __name__ == '__main__':
    cfg = Config()
    test_api = get_api(config=cfg)
    test_stream_listener = RetweetStreamListener(test_api)
    test_stream_listener.stream_tweets_from_keywords(['Python', 'JavaScript', 'OSS'])
