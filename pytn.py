import os

from flask import current_app, Flask, redirect, render_template, request
from werkzeug.contrib.cache import SimpleCache


ONE_HOUR = 3600


app = Flask(__name__)
cache = SimpleCache()

app.config.update(
    DEBUG=os.environ.get('APP_ENV', 'dev').lower() == 'dev',
    TESTING=os.environ.get('APP_ENV', 'dev').lower() == 'dev'
)

@app.before_request
def enforce_ssl_and_www():
    if not current_app.debug:
        host = request.host
        needs_www = not host.startswith('www.')
        needs_ssl = not current_app.is_secure

        if needs_www:
            host = 'www.%s' % host

        if needs_ssl or needs_www:
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
