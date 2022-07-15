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
```

```shell
$ venv
$ source venv/bin/activate
```

- Install the package dependencies.

```shell
$ pip install -r requirements.txt
```

- Set up your [Twitter OAuth](https://developer.twitter.com/en/docs/basics/authentication/overview) keys on your environment (`.env`)

```shell
API_KEY = ''
API_SECRET_KEY = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
```

- Run the bot.

```shell
$ python main.py
```
