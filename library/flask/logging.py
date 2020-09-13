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
        """
        Select logs
        ---
        parameters:
        - in: header
          name: X-IDENTIFIER
          required: true
          type: string

        - in: header
          name: X-ENVIRONMENT
          required: true
          type: string

        - in: header
          name: X-SECRET-KEY
          required: true
          type: string

        - in: query
          name: binds
          required: true
          description: using multiply id's, separated it by comma
          type: string

        - in: query
          name: limit
          type: integer
          minimum: 1
          maximum: 1000
          default: 0

        - in: query
          name: skip
          type: integer
          default: 0


        responses:
          200:
            description: OK

          417:
            description: Expectation Failed
        """

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
        """
        Insert new log
        ---
        parameters:
        - in: header
          name: X-IDENTIFIER
          required: true
          type: string

        - in: header
          name: X-ENVIRONMENT
          required: true
          type: string

        - in: header
          name: X-SECRET-KEY
          required: true
          type: string

        - in: body
          name: single log entry
          schema:
            type: object
            properties:
              summary:
                type: string
              description:
                type: string
              created_at:
                type: string
              tags:
                type: array
                items:
                  type: string
              binds:
                type: array
                items:
                  type: string
              system:
                type: boolean
              author:
                type: object
                properties:
                  name:
                    type: string
                  identifier:
                    type: string
                  ipv4:
                    type: string
                  ipv6:
                    type: string
        responses:
          200:
            description: OK

          417:
            description: Expectation Failed
        """

        logging.debug('FlaskLogging.create - request hit')

        identifier = request.headers.get('X-IDENTIFIER')
        environment = request.headers.get('X-ENVIRONMENT')

        data = request.get_json()

        response, msg = Logging.insert(data=data, identifier=identifier, environment=environment)
        return FlaskLogging.__return_response(response=response, msg=msg)

    @staticmethod
    def remove() -> (Response, int):
        """
        Remove a single log
        ---
        parameters:
          - in: header
            name: X-IDENTIFIER
            required: true
            schema:
              type: string

          - in: header
            name: X-ENVIRONMENT
            required: true
            type: string

          - in: header
            name: X-SECRET-KEY
            required: true
            type: string

          - in: query
            name: id
            required: true
            type: string

        responses:
          200:
            description: OK

          404:
            description: Not Found

          417:
            description: Expectation Failed
        """

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
