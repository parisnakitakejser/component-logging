import logging
from flask import Response
from bson.json_util import dumps


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

        return Response(dumps({
            'status': 'OK'
        }), mimetype='text/json'), 200

    @staticmethod
    def remove():
        logging.debug('FlaskLogging.remove - request hit')

        return Response(dumps({
            'status': 'OK'
        }), mimetype='text/json'), 200
