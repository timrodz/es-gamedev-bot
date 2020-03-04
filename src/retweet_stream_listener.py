import logging

from config import Config
from src.stream_listener import StreamListener
from src.twitter_api import get_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class RetweetStreamListener(StreamListener):
    def can_interact_with_tweet(self, tweet) -> bool:
        # Ignore tweet if it's either mine or a reply
        if tweet.user.id == self.me.id:
            logger.info(f'Skipping tweet: {tweet.id} (mine or reply to me)')
            return False
        
        # Ignore tweet if it's a quote retweet
        if tweet.is_quote_status:
            logger.info(f'Skipping tweet: {tweet.id} (quoted status)')
            return False

        # Ignore tweet if it has no likes
        if tweet.favorite_count < 1:
            logger.info(f'Skipping tweet: {tweet.id} (no likes)')
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
    test_api = get_api(cfg)
    test_stream_listener = RetweetStreamListener(test_api)
    test_stream_listener.stream_tweets_from_keywords(['Python', 'JavaScript', 'OSS'])
