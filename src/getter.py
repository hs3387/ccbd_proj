import boto3
import json

def lambda_handler(event, context):

    print(f"event: {event}")

    # create a DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # get references to the DynamoDB tables
    label_table = dynamodb.Table('clothing_labels')
    match_table = dynamodb.Table('clothing_recommendations')
    search_table = dynamodb.Table('clothing_search')
    user_table = dynamodb.Table('clothing_users')

    user = event["queryStringParameters"]["user"]
    page = int(event["queryStringParameters"]["page"])
    
    listIDs = list(user_table.get_item(Key={'id': user})['Item']['keys'])
    
    print("NAME-------------")
    print(listIDs)
    print(listIDs[page-1])
    print("DONEEE")
    
    return {
        'statusCode': 200,
        'body': "done"
    }
