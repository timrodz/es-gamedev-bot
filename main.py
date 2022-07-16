import logging
import os

from dotenv import load_dotenv

from src.stream import Stream

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


if __name__ == "__main__":
    keywords = [
        "#gamedev",
        "#indiedev",
        "#madewithunity",
        "#UE4",
        "#gamedev español",
    ]

    languages = ["es"]

    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_SECRET_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    stream = Stream(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
    )
    stream.filter(
        track=keywords, languages=languages, filter_level="low")
