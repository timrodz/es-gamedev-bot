import os

from dotenv import load_dotenv
from structlog import get_logger

from src.stream import Stream

load_dotenv()
log = get_logger()


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
    filter_level = os.getenv("FILTER_LEVEL", None)

    log.info("Initializing stream")
    stream = Stream(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
    )
    log.info("Starting stream", keywords={', '.join(keywords)},
             languages={', '.join(languages)}, filter_level=filter_level)
    stream.filter(track=keywords, languages=languages,
                  filter_level=filter_level)
