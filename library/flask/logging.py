import logging
from flask import Response, request
from bson.json_util import dumps

from library.logging import Logging


class FlaskLogging:
    @staticmethod
    def __return_response(response: bool, msg: str) -> (Response, int):
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
    def get() -> (Response, int):
        logging.debug('FlaskLogging.get - request hit')

        identifier = request.headers.get('X-IDENTIFIER')
        environment = request.headers.get('X-ENVIRONMENT')

        response, content, msg = Logging.get(data=request.args, identifier=identifier, environment=environment)

        if response:
            return Response(dumps({
                'status': 'OK',
                'content': content,
            }), mimetype='text/json'), 200
        else:
            return Response(dumps({
                'status': 'Expectation Failed',
                'msg': msg
            }), mimetype='text/json'), 417

    @staticmethod
    def create() -> (Response, int):
        logging.debug('FlaskLogging.create - request hit')

        identifier = request.headers.get('X-IDENTIFIER')
        environment = request.headers.get('X-ENVIRONMENT')

        data = request.get_json()

        response, msg = Logging.insert(data=data, identifier=identifier, environment=environment)
        return FlaskLogging.__return_response(response=response, msg=msg)

    @staticmethod
    def remove() -> (Response, int):
        logging.debug('FlaskLogging.remove - request hit')

        identifier = request.headers.get('X-IDENTIFIER')
        environment = request.headers.get('X-ENVIRONMENT')

        log_id = request.args.get('id')
        if log_id:
            response, msg = Logging.remove(log_id=log_id, identifier=identifier, environment=environment)
            return FlaskLogging.__return_response(response=response, msg=msg)
        else:
            return Response(dumps({
                'status': 'Not Found'
            }), mimetype='text/json'), 404
