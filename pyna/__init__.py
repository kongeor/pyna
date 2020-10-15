import os

from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    secret_key = os.getenv('SECRET_KEY')
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        DATABASE=os.path.join(app.instance_path, 'pyna.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database import init_db, db_session
    init_db()

    from .models import Headline

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from . import fetcher
    fetcher.init_app(app)

    @app.route('/api/fetch-headlines')
    def fetch_headlines():
        # TODO security
        # overcome single thread sqlite limitation
        fetcher.fetch_headlines()
        return "ok"

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def index():
        headlines = Headline.query.all()
        return render_template('index.html', headlines = headlines)

    return app
