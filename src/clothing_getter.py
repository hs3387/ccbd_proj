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
    
    print(user_table.get_item(Key={'id': user})['Item']['photos'])
    
    listIDs = list(user_table.get_item(Key={'id': user})['Item']['photos'])
    
    print("NAME-------------")
    print(listIDs)
    print(listIDs[page-1])

    search_str = search_table.get_item(Key={'key': listIDs[page-1]})
    label_str = label_table.get_item(Key={'key': listIDs[page-1]})
    match_str = match_table.get_item(Key={'key': listIDs[page-1]})
    

    print('len', len(listIDs))
    suggestion = search_str['Item']
    
    titles = []
    thumbnail = []
    price = []
    rating = []
    url = []
    stores = []
    favs = None
    for k,v in suggestion.items():
        if k != 'key'and k!='favs':
            titles.append(v["title"])
            thumbnail.append(v['thumbnail'])
            if v['delivery']:
                price.append(str(v['price']) + '(' + v['delivery'] + ')')
            rating.append(v['product_rating'])
            url.append(v['product_link'])
            stores.append(v['store'])
        elif k == 'favs':
            favs = v

    titles = titles[3:] + titles[:3]
    thumbnail = thumbnail[3:] + thumbnail[:3]
    price = price[3:] + price[:3]
    rating = rating[3:] + rating[:3]
    url = url[3:] + url[:3]
    stores = stores[3:] + stores[:3]


    s3 = boto3.client('s3')
    bucket_name = 'cloud-photos-b2'
    image_url = s3.generate_presigned_url('get_object', Params={'Bucket':bucket_name, 'Key':listIDs[page-1]})

    print("DONEEE")
    final = [titles, thumbnail, price, rating, url, image_url, label_str['Item']['labels'], len(listIDs), stores, favs]
    print(final)
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
        'body': json.dumps(final)
        
    }
