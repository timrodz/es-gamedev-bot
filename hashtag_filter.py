import typing

_hashtag_block_list: typing.List[str] = [
    "NFT"
]


def tweet_contains_blocked_hashtag(hashtags: typing.List[typing.Dict[str, str]]) -> bool:
    """
    We want to block any tweet that contains a remote hashtag match with any of our items inside the blocklist
    If our tweet contains the hashtag "NFT", we 1-1 match it against our item "NFT"
    If it has "NFT1", it also needs to be blocked because it matches "NFT"
    If it only contains an "N", we do not watch to block it because that doesn't match "NFT"
    """
    _hashtag_list: typing.List[str] = [hashtag["text"].upper() for hashtag in hashtags]

    return any(h for h in _hashtag_list if any(bh in h for bh in _hashtag_block_list))
