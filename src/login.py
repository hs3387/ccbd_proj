import boto3

def signin(usersTable, user, password):
    
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
    
    try: 
        userresponse = usersTable.get_item(Key={'id': user})
        if 'Item' in userresponse:
            return "User Already Exists"
    except:
        print("proceed")
    
    
    try: 
        usersTable.put_item(Item={'id': user, 'password': password})
    except:
        return "User Creation Failed"
    
    return "User Created"
    


def lambda_handler(event, context):
    
    print(f"event is THIS: {event}")
    # Extract the event data
    event_type = event['queryStringParameters']['type']
    user = event['queryStringParameters']['user']
    password = event['queryStringParameters']['pass']
    
    # Connect to the DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    usersTable = dynamodb.Table('clothing_users')
    
    if event_type == "signin":
        result = signin(usersTable, user, password)
    elif event_type == "signup":
        result = signup(usersTable, user, password)
    else:
        return{
        'statusCode': 400,
        'body': "INVALID USAGE"
        }
    
    return {
        'statusCode': 200,
        'body': result
    }
    