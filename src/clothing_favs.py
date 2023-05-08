import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('clothing_search')

def lambda_handler(event, context):
    print(event)
    # Get the key and faves from the PUT request body
    body = json.loads(event['body'])
    key = body['key']
    faves = body['faves']
    print(faves)
    
    # Split the faves string into a list with 5 strings
    fav_list = [faves[i:i+1] for i in range(0, len(faves), 1)]
    print(fav_list)
    
    # Update the item in the DynamoDB table
    table.update_item(
        Key={
            'key': key
        },
        UpdateExpression='SET favs = :val1',
        ExpressionAttributeValues={
            ':val1': fav_list
        }
    )
    
    # Return a response
    response = {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
        'body': json.dumps('Item updated successfully')
    }
    
    return response
