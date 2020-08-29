import os
import logging
from flask import Flask
import dotenv

dotenv.load_dotenv()

debug_mode = True if os.getenv('DEBUG_MODE') == '1' else False

if debug_mode:
    logging.basicConfig(level=logging.DEBUG)

from library.flask.logging import FlaskLogging

app = Flask(__name__)
# app.wsgi_app = 'db-conn'

app.add_url_rule('/logging', view_func=FlaskLogging.get, endpoint='logging_get', methods=['GET'])

if __name__ == '__main__':
    app.run('0.0.0.0', '5000', debug=debug_mode)