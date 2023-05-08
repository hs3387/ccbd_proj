import boto3
from label2suggestion import get_match, get_dresses
from product_suggestions import get_suggested_search_data
from collections import defaultdict
import json
import random

def detect_labels(photo, bucket, clothes):

     client = boto3.client('rekognition',region_name='us-east-1')

     response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
     MaxLabels=10,
     # Uncomment to use image properties and filtration settings
     Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
     #Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
     # "ImageProperties": {"MaxDominantColors":10}}
     )
    
     print('Detected labels for ' + photo)
     bounding_box = defaultdict(list)
     gender = 'unisex'
     
     for label in response['Labels']:
        #  print("LABEL =",label)
         print("Label: " + label['Name'])
         print("Confidence: " + str(label['Confidence']))
         print("Instances:")
         if label['Name'] == 'Female' or label['Name'] == 'Woman':
             gender = 'female'
         elif label['Name'] == 'Male' or label['Name'] == 'Man':
             gender = 'male'
         for instance in label['Instances']:
             
             print(" Bounding box")
             print(" Top: " + str(instance['BoundingBox']['Top']))
             print(" Left: " + str(instance['BoundingBox']['Left']))
             print(" Width: " + str(instance['BoundingBox']['Width']))
             print(" Height: " + str(instance['BoundingBox']['Height']))
             print(" Confidence: " + str(instance['Confidence']))
             print()

             if label['Name'] in clothes:
                 print("######APPENDING#########")
                 bounding_box[label['Name']].append(instance['BoundingBox'])

        #  print("Parents:")
        #  for parent in label['Parents']:
        #     print(" " + parent['Name'])
         
        #  print("Aliases:")
        #  for alias in label['Aliases']:
        #      print(" " + alias['Name'])

        #      print("Categories:")
        #  for category in label['Categories']:
        #      print(" " + category['Name'])
        #      print("----------")
        #      print()

     if "ImageProperties" in str(response):
        #  print("IMAGEPROPERTIES =",response["ImageProperties"])
         if 'Foreground' in response["ImageProperties"].keys():
             print("Background:")
             print(response["ImageProperties"]["Background"]["DominantColors"][0])
             print()
             print("Foreground:")
             print(response["ImageProperties"]["Foreground"]["DominantColors"][0])
             print()
            #  print("Quality:")
            #  print(response["ImageProperties"]["Quality"])
            #  print()
             
             return response['Labels'], response["ImageProperties"]["Foreground"]["DominantColors"][0]["CSSColor"], response["ImageProperties"]["Foreground"]["DominantColors"][0]["SimplifiedColor"], gender, bounding_box
         else:
             return response['Labels'], response["ImageProperties"]["DominantColors"][0]["CSSColor"], response["ImageProperties"]["DominantColors"][0]["SimplifiedColor"], gender, bounding_box

     return response['Labels'], None, None, gender, bounding_box



def run(user='testuser1',bucket = "cloud-photos-b2", photo = "green-blouse.jpg",max_matches=3):
    # TODO implement
    # bucket = "cloud-photos-b2"
    # photo = "green-blouse.jpg"
    clothing_items = get_dresses()
    print("SUPPORTED CLOTHES :")
    print(clothing_items)

    labels, csscolor, color, gender, bounding_boxes = detect_labels(photo,bucket,clothing_items)
    
    cloth_item = "clothing"
    
    found_flag = False
    for label in labels:
        for item in clothing_items:
            if item.lower() == label["Name"].lower():
                cloth_item = item
                found_flag = True
                break
        if found_flag:
            break
    
    if cloth_item == 'clothing':
        client = boto3.client('s3')
        response = client.delete_object(Bucket=bucket,Key=photo)
        print("No Clothing Detetcted ! :")
        print(response)
        return
    
    print("BOUNDING BOXES :")
    print(bounding_boxes)
    
    cloth_label = None
    
    for key in bounding_boxes.keys():
        print("LABEL :",key)
        print("BBs :")
        print(bounding_boxes[key])  
        cloth_label = key  
        break
    
    if cloth_label == cloth_item:
        client = boto3.client('lambda')
        
        inputParams = {
            "BoundingBoxes"   : bounding_boxes[cloth_label],
            "Bucket"      : bucket,
            "Photo"     : photo
        }
     
        response = client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-1:914175110612:function:color-identify',
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )
     
        responseFromChild = json.load(response['Payload'])
     
        print('RESPONSEFROMCHILD\n')
        print(responseFromChild)
        
        if 'statusCode' in responseFromChild.keys():
            if responseFromChild['statusCode'] == 200:
                colorResponse = responseFromChild['body']
                csscolor = colorResponse[0]
                color = colorResponse[1]
        
    # print("LABELS =",labels)

    # color = 'Forest Green'
    csscolor = csscolor.lower().replace("grey","gray")
    color = color.lower().replace("grey","gray")
    
    cloth_item = cloth_item.lower()
    # cloth_item = 'Blazer'
    print(color,cloth_item,"detected!")
    
    suggestions_data = get_suggested_search_data([gender,color,cloth_item],num_sugg=2)
    for i, sugg in enumerate(suggestions_data):
        print("Suggestion #",i+1,":",sugg['title'])
        
    matches = get_match([csscolor,cloth_item])
    if not matches:
        matches = get_match([color,cloth_item])
    print("#Matches =",len(matches))
    if len(matches) >= max_matches:
        matches = random.choices(matches,k=max_matches)
        print("Matches:")
        for match in matches:
            print(match)
    
            suggestions_data += get_suggested_search_data([gender]+match.split(" "))
            
    else:
        print("Matches:")
        for match in matches:
            print(match)
    
            suggestions_data += get_suggested_search_data([gender]+match.split(" "))
        
        suggestions_data += get_suggested_search_data([gender]+['Blue', 'Jeans'],num_sugg=max_matches-len(matches))
        
    print("#SUGG",len(suggestions_data))
    
    print("\nSUGGESTIONS:\n")
    for i, sugg in enumerate(suggestions_data):
        print("Suggestion #",i+1,":")
        print("Name :",sugg['title'])
        print("Thumbnail :",sugg['thumbnail'])
        print("Product URL :",sugg['product_link'])
        print("Price :",sugg['price'])
        print("Product Rating :",sugg['product_rating'])
    
    
    # Set up a DynamoDB resource
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('clothing_users')
    response = table.get_item(Key={'id':user})
    if 'Item' in response.keys():
        key_list = response["Item"]['photos']
        while photo in key_list:
            key_list.remove(photo)
        key_list = [photo]+key_list
        response = table.update_item(
            Key={
                'id': user
            },
            UpdateExpression='SET photos = :key_list',
            ExpressionAttributeValues={
                ':key_list': key_list
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Updated user",user,":",key_list)
    else:

        user_row = {
            "id" : user, "photos" : [photo]
        }

        print("Adding to clothing_users :",user_row)

        table.put_item(Item=user_row)


    # Set up a table object
    table = dynamodb.Table('clothing_labels')

    identified_label_row = {
        "key" : photo, "labels" : [color,cloth_item]
    }

    print("Adding to clothing_labels :",identified_label_row)

    table.put_item(Item=identified_label_row)

    if matches:
        table = dynamodb.Table('clothing_recommendations')

        reco_row = {
            "key" : photo, "recos" : matches
        }

        print("Adding to clothing_recommendations :",reco_row)

        table.put_item(Item=reco_row)
    if suggestions_data:
        table = dynamodb.Table('clothing_search')

        search_row = {
            "key" : photo,
            "favs" : ['0']*5
        }
        
        for i in range(len(suggestions_data)):
            search_row["suggestion_"+str(i)] = suggestions_data[i]

        print("Adding to clothing_search :",search_row["key"])

        table.put_item(Item=search_row)

    return

# results = run(user='haya',photo="blue_blouse.jpg")

def lambda_handler(event,context):
    print("EVENT:",event)
    print("context:",context)
    
    
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    key = key.replace("+"," ")
    try:
        s3 = boto3.client('s3')
        response = s3.head_object(Bucket=bucket,Key=key)
        user = response["ResponseMetadata"]["HTTPHeaders"]["x-amz-meta-customlabels"]
    except:
        print("Unable to retrieve User ID from Metadata")
        user = 'testuser'

    run(user,bucket,key)
    return