import logging
from werkzeug.wrappers import Response, Request
from mongoengine import DoesNotExist

from odm.authentication import Authentication as OdmAuthentication


class Authentication:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            identifier = environ.get('HTTP_X_IDENTIFIER')
            environment = environ.get('HTTP_X_ENVIRONMENT')
            secret_key = environ.get('HTTP_X_SECRET_KEY')

            logging.debug(f'Authentication identifier: {identifier}')
            logging.debug(f'Authentication environment: {environment}')
            logging.debug(f'Authentication secret_key: {secret_key}')

            if not identifier or not environment or not secret_key:
                logging.error('Authentication missing identifier, environment or secret_key in the headers')
                res = Response(u'Authentication - Missing header data', mimetype='text/plain', status=403)
                return res(environ, start_response)

            try:
                row = OdmAuthentication.objects.get(identifier=identifier, environment=environment, secret_key=secret_key)

                if not row.available:
                    logging.error('Authentication - Not Acceptable')
                    res = Response(u'Authentication - Not Acceptable', mimetype='text/plain', status=406)
                    return res(environ, start_response)

            except DoesNotExist:
                logging.error('Authentication - Unauthorized')
                res = Response(u'Authentication - Unauthorized', mimetype='text/plain', status=401)
                return res(environ, start_response)

        except Exception as e:
            logging.error('Authentication - Not Implemented')
            res = Response(u'Authentication - Not Implemented', mimetype='text/plain', status=501)
            return res(environ, start_response)

        logging.debug('Authentication - OK')
        return self.app(environ, start_response)