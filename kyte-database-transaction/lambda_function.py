import os
import json
import logging
from kyte import DBI

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Cache DB credentials
DB_HOST = os.environ['db_host']
DB_USERNAME = os.environ['db_username']
DB_PASSWORD = os.environ['db_password']

def db_connection(db_name):
    return DBI.MySql(DB_HOST, DB_USERNAME, DB_PASSWORD, db_name)

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            body = json.loads(record['body'])
            action = body.get('action')

            actions = {
                'insert': insert_function,
                'update': update_function,
                'delete': delete_function,
                'get': get_function,
            }

            result = actions.get(action, default_action)(body)
            logger.info(f"Action {action} executed with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Error processing the request'
        }

def insert_function(body):
    db = db_connection(body['db_name'])
    db.insert(body['param'])
    return {
        'statusCode': 200,
        'body': body['action']
    }

def update_function(body):
    db = db_connection(body['db_name'])
    db.update(body['param'])
    return {
        'statusCode': 200,
        'body': body['action']
    }
    
def delete_function(body):
    db = db_connection(body['db_name'])
    db.delete(body['param'])
    return {
        'statusCode': 200,
        'body': body['action']
    }

def get_function(body):
    db = db_connection(body['db_name'])
    result = db.get(body['param'])
    # Todo: implement way to return data
    return {
        'statusCode': 200,
        'body': body['action']
    }

def default_action(body):
    # Handle default action or invalid action
    return {
        'statusCode': 400,
        'body': 'Unknown action requested: '+body['action']
    }