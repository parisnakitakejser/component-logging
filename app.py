import os
import logging
from flask import Flask, jsonify, render_template
from flask_swagger import swagger
import dotenv

from library.flask.logging import FlaskLogging

from middleware.dbConnect import DBConnect
from middleware.authentication import Authentication

dotenv.load_dotenv()

debug_mode = True if os.getenv('DEBUG_MODE') == '1' else False

if debug_mode:
    logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.wsgi_app = Authentication(app.wsgi_app)
app.wsgi_app = DBConnect(app.wsgi_app)

app.add_url_rule('/logging', view_func=FlaskLogging.get, endpoint='logging_get', methods=['GET'])
app.add_url_rule('/logging', view_func=FlaskLogging.create, endpoint='logging_create', methods=['POST'])
app.add_url_rule('/logging', view_func=FlaskLogging.remove, endpoint='logging_remove', methods=['DELETE'])


@app.route('/docs')
def get_root():
    return render_template('swaggerui.html')


@app.route("/docs/swagger.json")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0 beta"
    swag['info']['title'] = "Logging API"
    return jsonify(swag)


if __name__ == '__main__':
    app.run('0.0.0.0', '5000', debug=debug_mode)
