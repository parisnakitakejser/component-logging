import logging
from flask import Response, request
from bson.json_util import dumps

from library.logging import Logging


class FlaskLogging:
    @staticmethod
    def get():
        logging.debug('FlaskLogging.get - request hit')

        return Response(dumps({
            'status': 'OK'
        }), mimetype='text/json'), 200

    @staticmethod
    def create():
        logging.debug('FlaskLogging.create - request hit')

        identifier = request.headers.get('X-IDENTIFIER')
        environment = request.headers.get('X-ENVIRONMENT')

        data = request.get_json()

        response, msg = Logging.insert(data=data, identifier=identifier, environment=environment)

        if response:
            logging.debug(msg)

            return Response(dumps({
                'status': 'OK'
            }), mimetype='text/json'), 200
        else:
            logging.error(msg)

            return Response(dumps({
                'status': 'Expectation Failed',
                'msg': msg
            }), mimetype='text/json'), 417

    @staticmethod
    def remove():
        logging.debug('FlaskLogging.remove - request hit')

        return Response(dumps({
            'status': 'OK'
        }), mimetype='text/json'), 200
