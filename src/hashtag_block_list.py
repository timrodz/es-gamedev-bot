"""
We want to block any tweet that contains a remote hashtag match with any of our items inside the blocklist
If our tweet contains the hashtag "NFT", we 1-1 match it against our item "NFT"
If it has "NFT1", it also needs to be blocked because it matches "NFT"
If it only contains an "N", we do not watch to block it because that doesn't match "NFT"
"""
import typing

block_list: typing.List[str] = ["NFT"]
