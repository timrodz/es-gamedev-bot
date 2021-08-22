import logging
import tweepy

from config import Config
from src.twitter_api import get_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class StreamListener(tweepy.StreamListener):
    def __init__(self, api: tweepy.API):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f'{tweet.user.name}:{tweet.text}')

    def on_error(self, status):
        logger.error(f'Error detected: {status}', exc_info=True)

    def stream_tweets_from_keywords(self, keywords: [str], languages: [str] = None, *args):
        if not languages:
            languages = ['en']

        logger.info(f'Streaming with keywords: {", ".join(keywords)} and language(s): {", ".join(languages)}')
        stream = tweepy.Stream(self.api.auth, self)
        stream.filter(track=keywords, languages=languages, is_async=True, *args)

    def stream_tweets_from_user(self, user_id: str):
        logger.info(f'Streaming with user ID: {user_id}')
        stream = tweepy.Stream(self.api.auth, self)
        stream.filter(follow=[user_id], is_async=True)


if __name__ == '__main__':
    cfg = Config()
    test_api = get_api(config=cfg)
    test_listener = StreamListener(test_api)
    test_listener.stream_tweets_from_keywords(['Python', 'Tweepy'])
