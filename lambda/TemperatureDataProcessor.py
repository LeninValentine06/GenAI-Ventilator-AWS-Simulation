import json
import logging
import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Lambda client
lambda_client = boto3.client('lambda')

# Replace this with your Lambda function ARN
TARGET_LAMBDA_ARN = 'arn:aws:lambda:region:account-id:function:function-name'

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        # Extract payload
        payload = event.get('payload', None) or event
        if isinstance(payload, str):
            payload = json.loads(payload)
        
        temperature_data = payload.get('TEMPERATURE') or payload.get('temperature')

        if temperature_data is not None:
            logger.info(f"Received temperature data: {temperature_data}")

            # Prepare the payload to send to the target Lambda function
            payload = {
                'body': json.dumps({'temperature': temperature_data})
            }

            # Invoke the target Lambda function synchronously
            try:
                response = lambda_client.invoke(
                    FunctionName=TARGET_LAMBDA_ARN,
                    InvocationType='RequestResponse',  # Use 'RequestResponse' for synchronous invocation
                    Payload=json.dumps(payload)
                )
                response_payload = json.loads(response['Payload'].read())
                logger.info(f"Invoke response: {response_payload}")
            except Exception as e:
                logger.error(f"Error invoking target Lambda function: {e}")
                return {'statusCode': 500, 'body': 'Failed to invoke target Lambda function'}

        else:
            logger.error("No temperature data found in the event")
            return {'statusCode': 400, 'body': 'No temperature data found'}

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return {'statusCode': 400, 'body': 'Invalid JSON format'}
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {'statusCode': 500, 'body': 'Internal Server Error'}
    
    return {'statusCode': 200, 'body': 'Data processed and sent successfully'}
