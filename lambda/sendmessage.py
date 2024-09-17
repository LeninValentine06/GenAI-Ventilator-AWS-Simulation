import json
import boto3

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))
    
    # Extract and parse the message from the event
    try:
        body = event.get('body', '{}')
        message_data = json.loads(body)  # Parse the JSON string
        print(f"Parsed message data: {message_data}")
        
        # Extract the temperature value
        temperature = message_data.get('temperature', None)
        if temperature is None:
            return {
                'statusCode': 400,
                'body': 'Temperature data not found in the message'
            }
        
        # Format the message for WebSocket clients
        formatted_message = json.dumps({"temperature": temperature})
        print(f"Formatted message to send: {formatted_message}")
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {
            'statusCode': 400,
            'body': 'Invalid JSON format in the message'
        }
    
    # Your API Gateway WebSocket endpoint
    api_endpoint = 'your-api-endpoint'
    
    # Initialize API Gateway Management API client
    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=api_endpoint)
    
    # Get connection IDs from DynamoDB
    connection_ids = get_connected_clients()
    print("Connection IDs:", connection_ids)
    
    for connection_id in connection_ids:
        try:
            # Send the formatted message to the client
            response = apig_management_client.post_to_connection(
                ConnectionId=connection_id,
                Data=formatted_message
            )
            print(f"Message sent to {connection_id}: {response}")
        except Exception as e:
            print(f"Failed to send message to {connection_id}: {e}")
    
    return {
        'statusCode': 200,
        'body': 'Message sent to all clients'
    }

def get_connected_clients():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('WebSocketConnections')
    
    # Scan the table to get all connection IDs
    response = table.scan()
    print("DynamoDB scan response:", json.dumps(response, indent=2))
    connection_ids = [item['ConnectionId'] for item in response.get('Items', [])]
    
    return connection_ids
