import requests
import click
from flask.cli import with_appcontext
from datetime import datetime
from dotenv import load_dotenv
import os

from . import db as dbm

def date_to_ts(date_str):
	d = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
	return int(d.timestamp())


@click.command('fetch-hl')
@with_appcontext
def fetch_headlines():
	db = dbm.get_db()

	news_api_keys = os.getenv('NEWS_API_KEY')

	r = requests.get('https://newsapi.org/v2/top-headlines?country=gr&pageSize=30&apiKey=%s' % (news_api_keys))

	max_pub_at = db.execute('SELECT MAX(published_at_ts) as max_ts from headlines').fetchone()

	max_ts = max_pub_at['max_ts']
	
	headlines = r.json()['articles']

	if max_ts:
		filtered = list(filter(lambda h: date_to_ts(h['publishedAt']) > max_ts, headlines))
	else:
		filtered = headlines

	# TODO logs
	print("Saving " + str(len(filtered)) + " headlines")

	for hl in filtered:
		published_at = date_to_ts(hl['publishedAt'])
		
		db.execute(
				'INSERT INTO headlines (source_id, source_name, author, title, description, url, url_to_image, published_at_ts, published_at, content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
				(hl['source']['id'], hl['source']['name'], hl['author'], hl['title'], hl['description'], hl['url'], hl['urlToImage'], published_at, hl['publishedAt'], hl['content'])
			)
	db.commit()

def init_app(app):
    app.cli.add_command(fetch_headlines)
