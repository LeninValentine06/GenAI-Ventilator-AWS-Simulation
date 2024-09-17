import logging
import boto3
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WebSocketConnections')

def lambda_handler(event, context):
    logger.info(f"Event: {event}")
    logger.info(f"Context: {context}")

    # Check if 'requestContext' exists in the event
    if 'requestContext' not in event:
        return {
            'statusCode': 400,
            'body': 'Bad Request: Missing requestContext.'
        }

    # Extract connection ID
    connection_id = event['requestContext'].get('connectionId', None)
    
    if not connection_id:
        return {
            'statusCode': 400,
            'body': 'Bad Request: Missing connectionId.'
        }
    
    # Log the connection ID
    logger.info(f"Connected with connection ID: {connection_id}")

    try:
        # Add connection ID to DynamoDB
        table.put_item(Item={'ConnectionId': connection_id})
        logger.info(f"Connection ID {connection_id} added to DynamoDB")
    except ClientError as e:
        logger.error(f"Error adding connection ID to DynamoDB: {e}")
        return {
            'statusCode': 500,
            'body': 'Internal Server Error: Unable to connect.'
        }

    # Return success response
    return {
        'statusCode': 200,
        'body': 'Connected successfully.'
    }
