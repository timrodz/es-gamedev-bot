from config import Config
from src import twitter_api
from src import retweet_stream_listener

if __name__ == '__main__':
    keywords = [
        '#gamedev',
        '#indiedev',
        '#madewithunity',
        '#UE4',
        '#gamedev español',
    ]

    languages = ['es']

    cfg = Config()
    api = twitter_api.get_api(config=cfg)
    stream_listener = retweet_stream_listener.RetweetStreamListener(api)
    stream_listener.stream_tweets_from_keywords(keywords, languages)
