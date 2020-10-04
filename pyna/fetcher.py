import requests
import click
from flask.cli import with_appcontext
from datetime import datetime
from dotenv import load_dotenv
import os

from sqlalchemy.sql.expression import func

from .database import db_session
from .models import Source, Headline

def date_to_ts(date_str):
	d = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
	return int(d.timestamp())


@click.command('fetch-hl')
@with_appcontext
def fetch_headlines():

	news_api_keys = os.getenv('NEWS_API_KEY')

	r = requests.get('https://newsapi.org/v2/top-headlines?country=gr&pageSize=30&apiKey=%s' % (news_api_keys))

	Headline.query.order_by

	top_headline = Headline.query.order_by(Headline.published_at_ts.desc()).first()
	
	headlines = r.json()['articles']

	if top_headline:
		max_ts = top_headline.published_at_ts
		filtered = list(filter(lambda h: date_to_ts(h['publishedAt']) > max_ts, headlines))
	else:
		filtered = headlines

	# TODO logs
	print("Saving " + str(len(filtered)) + " headlines")

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

def init_app(app):
    app.cli.add_command(fetch_headlines)
