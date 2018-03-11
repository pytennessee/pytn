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
def enforce_ssl_and_www():
    if not current_app.debug:
        host = request.host
        if not host.startswith('www.'):
            host = 'www.%s' % host

        return redirect('{protocol}{host}{path}'.format(
            protocol='https://',
            host=host,
            path=request.path
        ))


@app.route('/', methods=['GET'])
def index():
    page = cache.get('index-page')
    if page is None:
        page = render_template('index.html')
        cache.set('index-page', page, timeout=ONE_HOUR)
    return page
