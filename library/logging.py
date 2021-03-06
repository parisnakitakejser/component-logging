import logging
from datetime import datetime
from mongoengine import DoesNotExist

from odm.logging import Logging as OdmLogging, LoggingData as OdmLoggingData
from odm.author import Author as OdmAuthor


class Logging:
    @staticmethod
    def insert(data: dict, identifier: str, environment: str) -> (bool, str):
        if 'created_at' not in data or not data['created_at']:
            created_at = datetime.utcnow()
        else:
            try:
                created_at = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                return False, 'created_at did not contain the right date format - %Y-%m-%d %H:%M:%S'

        if 'description' in data and type(data['description']) != str:
            return False, 'Your description need to be a string'

        if 'summary' not in data or not data['summary']:
            return False, 'Your summary can\'t be empty'
        elif type(data['summary']) != str:
            return False, 'Your summary need to be a string'

        if 'binds' not in data or type(data['binds']) != list or len(data['binds']) == 0:
            return False, 'Your binds need to contain at lest 1 item'

        if 'system' in data and type(data['system']) != bool:
            return False, 'Your system need to be a boolean'

        log_data = OdmLoggingData()
        log_data.summary = data['summary']

        if 'description' in data:
            log_data.description = data['description']

        log_data.created_at = created_at

        author = None
        if 'author' in data:
            author_data = data['author']
            author = OdmAuthor()
            author.name = author_data['name']

            if 'identifier' in author_data:
                author.identifier = author_data['identifier']

            if 'ipv4' in author_data:
                author.ipv4 = author_data['ipv4']

            if 'ipv6' in author_data:
                author.ipv6 = author_data['ipv6']

        log = OdmLogging()
        log.identifier = identifier
        log.environment = environment
        log.data = log_data

        if author:
            log.author = author

        log.binds = data['binds']
        log.tags = data['tags'] if 'tags' in data else []
        log.created_at = datetime.utcnow()
        log.save()

        return True, 'Insert log message success'

    @staticmethod
    def remove(log_id: str, identifier: str, environment: str) -> (bool, str):
        try:
            log = OdmLogging.objects.get(pk=log_id)
        except DoesNotExist:
            return False, 'Log message not found'

        if log.identifier == identifier and log.environment == environment:
            log.update(**{
                'set__deleted_at': datetime.utcnow()
            })
            return True, 'Log message success removed'
        else:
            return False, 'You did not have the right access to delete this log message'

    @staticmethod
    def get(data: dict, identifier: str, environment: str) -> (bool, list, str):
        pipeline = []

        if 'binds' not in data or type(data['binds']) != str or len(data['binds'].split(',')) == 0:
            return False, [], 'binds missing data or incorrect format'

        limit = 100
        skip = 0

        if 'limit' in data:
            try:
                limit = int(data['limit'])
                logging.info(f'limit cast to int value: {limit}')
            except Exception as e:
                return False, [], 'limit need to be a int value'

            if limit < 1 or limit > 1000:
                return False, [], 'limit need to be between 1-1000'

        if 'skip' in data:
            try:
                skip = int(data['skip'])
            except Exception as e:
                return False, [], 'skip need to be a int value'

            if skip < 0:
                return False, [], 'skip shut be equal or greater then 0'

        pipeline.append({
            '$match': {
                'binds': {
                    '$in': data['binds'].split(',')
                },
                'deleted_at': {
                    '$exists': False
                }
            }
        })

        pipeline.append({
            '$sort': {
                'data.created_at': -1
            }
        })

        pipeline.append({
            '$skip': (skip * limit)
        })

        pipeline.append({
            '$limit': limit
        })

        return True, OdmLogging.objects(identifier=identifier, environment=environment).aggregate(pipeline), 'success mongo query'
