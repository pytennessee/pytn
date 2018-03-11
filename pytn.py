import os

from flask import current_app, Flask, redirect, render_template, request
from werkzeug.contrib.cache import SimpleCache


ONE_HOUR = 3600


app = Flask(__name__)
cache = SimpleCache()

app.config.update(
    DEBUG=os.environ.get('DEBUG', False),
    TESTING=os.environ.get('TESTING', False)
)

@app.before_request
def enforce_ssl():
    debug_enabled = current_app.debug
    if not (debug_enabled or request.is_secure):
        return redirect(request.url.replace("http://", "https://"))


@app.route('/', methods=['GET'])
def index():
    page = cache.get('index-page')
    if page is None:
        page = render_template('index.html')
        cache.set('index-page', page, timeout=ONE_HOUR)
    return page
