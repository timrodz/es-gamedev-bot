# ¡Gamedev en Español!

A bot that celebrates and promotes game development written in Spanish.

Inspired by [this Real Python post](https://realpython.com/twitter-bot-python-tweepy).

## Links

- [Twitter Account](https://twitter.com/EsGamedevBot).
- [Change Log](CHANGELOG.md).

## Development

- Create a virtual environment.

```shell
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
```

- Install project dependencies.

```shell
pip install -r requirements.txt
```

- Generate [Twitter OAuth](https://developer.twitter.com/en/docs/basics/authentication/overview) keys, and save them to an `.env` file:

```shell
API_KEY
API_SECRET_KEY
ACCESS_TOKEN
ACCESS_TOKEN_SECRET
```

- Run the bot.

```shell
python main.py
```
