import boto3
import json

def signin(usersTable, user, password):
    print("5")
    # Query the table for the user's ID
    try: 
        userresponse = usersTable.get_item(Key={'id': user})
        if 'Item' not in userresponse:
            raise ValueError("User Not Found")
        
    except:
        return "User Not Found"

    if password == userresponse['Item']['password']:
        result = "LOGIN SUCCESS"
    else:
        result = "LOGIN FAIL"

    return result

def signup(usersTable, user, password):
    print("6")

    try: 
        userresponse = usersTable.get_item(Key={'id': user})
        if 'Item' in userresponse:
            return "User Already Exists"
    except:
        print("proceed")
    
    
    try: 
        usersTable.put_item(Item={'id': user, 'password': password, 'photos':[]})
    except:
        return "User Creation Failed"
    
    return "User Created"
    


def lambda_handler(event, context):
    
    print(f"event is THIS: {event}")
    # Extract the event data
    event_type = event['queryStringParameters']['type']
    print(f"1{event_type}")
    user = event['queryStringParameters']['user']
    print(f"2{user}")
    password = event['queryStringParameters']['pass']
    print(f"3{password}")
    
    # Connect to the DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    usersTable = dynamodb.Table('clothing_users')
    
    print("4")
    
    if event_type == "signin":
        result = signin(usersTable, user, password)
    elif event_type == "signup":
        result = signup(usersTable, user, password)
    else:
        return{
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
        'body': json.dumps(result)
        }
    
    print(f"7{result}")
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
        'body': json.dumps(result)
    }
    