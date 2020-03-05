# ¡Gamedev en Español!

A bot that celebrates and promotes game development written in Spanish.

## Links

- [Twitter Account](https://twitter.com/EsGamedevBot).
- [Change Log](CHANGELOG.md).

## Development

- Create a virtual environment.

```shell
$ venv
$ source venv/bin/activate
```

- Install the package dependencies.

```shell
$ pip install -r requirements.txt
```

- Set up your [Twitter OAuth](https://developer.twitter.com/en/docs/basics/authentication/overview) keys on `config.py`.

```python
API_KEY = ''
API_SECRET_KEY = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
```

- Run the bot.

```shell
$ python main.py
```
