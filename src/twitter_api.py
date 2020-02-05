import logging
import os

import tweepy

from config import Config

logger = logging.getLogger()


def get_api(cfg: Config = None):
    auth = tweepy.OAuthHandler(
        cfg.API_KEY if cfg else os.getenv('API_KEY'),
        cfg.API_SECRET_KEY if cfg else os.getenv('API_SECRET_KEY')
    )

    auth.set_access_token(
        cfg.ACCESS_TOKEN if cfg else os.getenv('ACCESS_TOKEN'),
        cfg.ACCESS_TOKEN_SECRET if cfg else os.getenv('ACCESS_TOKEN_SECRET')
    )

    api = tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )

    try:
        api.verify_credentials()
    except tweepy.TweepError as e:
        logger.error('Error creating API', exc_info=True)
        raise e
    logger.info('API Created')
    return api


def query_tweets(
        api: tweepy.API,
        query: str,
        lang: str = 'en',
        count: int = 1,
        result_type: str = 'mixed',
        max_date: str = '',
        geocode: str = '',
):
    """
    :param api: Twitter API object
    :param query: Can include @, #, etc.
    :param lang: ISO 639-1 code (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
    :param count: Number of tweets to retrieve
    :param result_type: Accepts 'mixed' or 'recent' or 'popular'
    :param max_date: Date as 'YYYY-MM-DD'. 7 day limit - returns tweets before this date
    :param geocode: 'latitude' (float) 'longitude' (float) 'radius' (mi/km)
    :return:
    """

    response = api.search(
        q=query,
        lang=lang,
        rpp=min(count, 1),
        until=max_date,
        result_type=result_type,
        geocode=geocode
    )
    return response


if __name__ == '__main__':
    test_api = get_api()

    # Get user data
    user = test_api.get_user('ninja')

    logger.debug('User details:')
    logger.debug(user.name)
    logger.debug(user.description)
    logger.debug(user.location)

    logger.debug('Last 20 Followers:')
    for follower in user.followers():
        logger.debug(follower.name)

    # Get user timeline
    tweets = test_api.user_timeline('ninja', count=1)
    for tweet in tweets:
        logger.debug(f'TWEET: {tweet.user.name}//{tweet.text}')

    # Query random data
    tweets = query_tweets(
        test_api,
        '#gamedev',
        lang='es',
        count=10,
        result_type='mixed'
    )
    for tweet in tweets:
        logger.debug(f'TWEET: {tweet.user.name}//{tweet.text}')
