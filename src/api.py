import tweepy


def get_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    return tweepy.API(auth)
