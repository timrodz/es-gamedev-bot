import logging

from config import Config
from src.stream_listener import StreamListener
from src.twitter_api import get_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class RetweetStreamListener(StreamListener):
    def on_status(self, tweet):
        logger.info(f'Processing tweet id {tweet.id}')

        # Ignore tweet if it's either mine or a reply
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return

        # Like
        if not tweet.favorited:
            try:
                tweet.favorite()
                logger.info(f'Liked: {tweet.id}')
            except Exception as e:
                logger.error(f'Error on like: {e}', exc_info=True)
        # Retweet
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
