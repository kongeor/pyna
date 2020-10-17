import requests
import click
from flask.cli import with_appcontext
from datetime import datetime
from dotenv import load_dotenv
import os
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from sqlalchemy.sql.expression import func

from .database import db_session
from .models import Source, Headline

import logging

log = logging.getLogger('fetcher')

# Fetcher

def date_to_ts(date_str):
	d = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
	return int(d.timestamp())


def fetch_headlines():
	log.info("fetching headlines fron newsapi")
	news_api_keys = os.getenv('NEWS_API_KEY')

	r = requests.get('https://newsapi.org/v2/top-headlines?country=gr&pageSize=30&apiKey=%s' % (news_api_keys))

	Headline.query.order_by

	top_headline = Headline.query.order_by(Headline.published_at_ts.desc()).first()
	
	headlines = r.json()['articles']

	log.info("Got %s headlines from newsapi.org", (len(headlines)))

	max_ts = None

	if top_headline:
		max_ts = top_headline.published_at_ts
		filtered = list(filter(lambda h: date_to_ts(h['publishedAt']) > max_ts, headlines))
	else:
		filtered = headlines

	log.info("Saving %s headlines after %s", (len(filtered)), max_ts)

	for hl in filtered:
		source = Source.query.filter(Source.source_name == hl['source']['name']).first()
		if source is None:
			source = Source(source_id = hl['source']['id'], source_name = hl['source']['name'])

		published_at = date_to_ts(hl['publishedAt'])

		headline = Headline(source, 
			author = hl['author'], 
			title = hl['title'], 
			description = hl['description'], 
			url = hl['url'], 
			url_to_image = hl['urlToImage'], 
			published_at_ts = published_at, 
			published_at = hl['publishedAt'], 
			content = hl['content']
		)
		
		db_session.add(headline)
		# commit on each iteration to make sure Source is inserted
		db_session.commit()

@click.command('fetch-hl')
@with_appcontext
def fetch_headlines_cmd():
	fetch_headlines()

# Scheduler

sched = BackgroundScheduler(daemon=True)

sched.start()

atexit.register(lambda: sched.shutdown())

def poke_api():
	requests.get("http://localhost:5000/api/fetch-headlines")

def init_app(app):
	# poke_api()
	sched.add_job(poke_api, 'cron', minute="*/15")
	app.cli.add_command(fetch_headlines_cmd)
