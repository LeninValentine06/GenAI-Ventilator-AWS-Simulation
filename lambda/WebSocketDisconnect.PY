import boto3

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('WebSocketConnections')
    
    # Remove the connection ID from the table
    table.delete_item(Key={'ConnectionId': connection_id})
    
    return {
        'statusCode': 200,
        'body': 'Disconnected.'
    }
