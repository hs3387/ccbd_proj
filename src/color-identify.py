import json
import cv2
import numpy as np
import boto3

def detect_color(photo):

     client = boto3.client('rekognition',region_name='us-east-1')

     response = client.detect_labels(Image={'Bytes':photo},
     MaxLabels=10,
     # Uncomment to use image properties and filtration settings
     Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
     #Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
     # "ImageProperties": {"MaxDominantColors":10}}
     )
    
    #  print('Detected labels for ' + photo)
    #  bounding_box = defaultdict(list)
     for label in response['Labels']:
        #  print("LABEL =",label)
         print("Label: " + label['Name'])
         print("Confidence: " + str(label['Confidence']))
         print("Instances:")

         for instance in label['Instances']:
             
             print(" Bounding box")
             print(" Top: " + str(instance['BoundingBox']['Top']))
             print(" Left: " + str(instance['BoundingBox']['Left']))
             print(" Width: " + str(instance['BoundingBox']['Width']))
             print(" Height: " + str(instance['BoundingBox']['Height']))
             print(" Confidence: " + str(instance['Confidence']))
             print()

            #  if label['Name'] in clothes:
            #      bounding_box[label['Name']].append(instance['BoundingBox'])

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
         print("IMAGEPROPERTIES =",response["ImageProperties"].keys())
         if 'Foreground' in response["ImageProperties"].keys():
             print("Background:")
             print(response["ImageProperties"]["Background"]["DominantColors"][0])
             print()
             print("Foreground:")
             print(response["ImageProperties"]["Foreground"]["DominantColors"][0])
             print()
             return response["ImageProperties"]["Foreground"]["DominantColors"][0]["CSSColor"], response["ImageProperties"]["Foreground"]["DominantColors"][0]["SimplifiedColor"]
         elif 'DominantColors' in response["ImageProperties"].keys():
             print("Foreground:")
             print(response["ImageProperties"]["DominantColors"][0])
             print()
             return response["ImageProperties"]["DominantColors"][0]["CSSColor"], response["ImageProperties"]["DominantColors"][0]["SimplifiedColor"]
        #  print("Quality:")
        #  print(response["ImageProperties"]["Quality"])
        #  print()
         
         

     return None


def lambda_handler(event, context):
    # TODO implement
    print("EVENT")
    print(event)
    bounding_boxes = event["BoundingBoxes"]
    bucket = event['Bucket']
    photo = event['Photo']
    
    
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket)
    img = bucket.Object(photo).get().get('Body').read()
    image = cv2.imdecode(np.asarray(bytearray(img)), cv2.IMREAD_COLOR)

    # cv2.imshow('Final_Image',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    print(image.shape)

    bb = bounding_boxes[0]
    print(bb)
    Y = int(bb['Top']*image.shape[0])
    H = int(bb['Height']*image.shape[0])
    X = int(bb['Left']*image.shape[1])
    W = int(bb['Width']*image.shape[1])
    print([X,Y,W,H])
    cropped_image = image[Y:Y+H, X:X+W]
    

    # cv2.imshow('Cropped_Image',cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    retval, buffer = cv2.imencode('.jpg', cropped_image)
    # jpg_as_text = base64.b64encode(buffer)
    data_encode = np.array(buffer)
  
# Converting the array to bytes.
    jpg_as_text = data_encode.tobytes()
    # print(jpg_as_text)
    csscolor, color = detect_color(jpg_as_text)
    print("Corrected Color:")
    print("CSSColor :",csscolor)
    print("SimplifiedColor :",color)

    
    return {
        'statusCode': 200,
        'body': [csscolor,color]
    }
