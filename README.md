# pyna

## What is it?

`Pyna` is a small [flask](https://flask.palletsprojects.com/en/1.1.x/) service for serving
the latest headlines provided by [newsapi.org](https://newsapi.org/).

## Is it good?

[Yes.](https://news.ycombinator.com/item?id=3067434)


## Development

### First time setup

Prepare your `.env` file:

```sh
cp .env.example .env
```

Signup and get a [newsapi.org](https://newsapi.org/) API key and update your `.env` file.


You will need [pipenv](https://pypi.org/project/pipenv/) to setup your environment and
dependencies.

Start a shell:

```sh
pipenv shell
```

Install dependencies:

```sh
pipenv install
```

### Executing

When your env is ready, you will only need to start a shell:

```sh
pipenv shell
```

and start flask:

```
flask run
```

and point your browser to `http://127.0.0.1:5000/`!

But wait! There is nothing there, just an empty headline.

### Fetch some news

Run the fetch headlines command to fetch some news:

```
flask fetch-hl
```


## License

[AGPLv3](LICENSE)








