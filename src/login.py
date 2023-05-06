import boto3

def lambda_handler(event, context):
    # Extract the event data
    event_type = event['type']
    user = event['user']
    password = event['pass']
    
    # Print the extracted data
    print(f"Event type: {event_type}")
    print(f"User: {user}")
    print(f"Password: {password}")
    
    # Connect to the DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('clothing_user')
    
    # Query the table for the user's ID
    response = table.get_item(
        Key={
            'id': user
        }
    )
    
    # Extract the ID from the response
    user_id = response['Item']['id']
    
    # Print the user's ID
    print(f"User ID: {user_id}")
    
    # Return a response
    return {
        'statusCode': 200,
        'body': f"User ID: {user_id}"
    }
