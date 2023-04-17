import boto3
from label2suggestion import get_match
from product_suggestions import get_suggested_search_data

def detect_labels(photo, bucket):

     client = boto3.client('rekognition',region_name='us-east-1')

     response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
     MaxLabels=10,
     # Uncomment to use image properties and filtration settings
     Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
     #Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
     # "ImageProperties": {"MaxDominantColors":10}}
     )

     print('Detected labels for ' + photo)
     
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
         print("Background:")
         print(response["ImageProperties"]["Background"]["DominantColors"][0])
         print()
         print("Foreground:")
         print(response["ImageProperties"]["Foreground"]["DominantColors"][0])
         print()
        #  print("Quality:")
        #  print(response["ImageProperties"]["Quality"])
        #  print()
         
         return response['Labels'], response["ImageProperties"]["Foreground"]["DominantColors"][0]["SimplifiedColor"]

     return response['Labels'], None


def run(bucket = "cloud-photos-b2", photo = "green-blouse.jpg"):
    # TODO implement
    bucket = "cloud-photos-b2"
    photo = "green-blouse.jpg"
    
    labels, color = detect_labels(photo,bucket)
    # print("LABELS =",labels)
    
    clothing_items = ["Shirt", "T-Shirt", "Jeans", "Pants", "Blouse", "Skirt"]
    
    cloth_item = "clothing"
    
    found_flag = False
    for label in labels:
        for item in clothing_items:
            if item == label["Name"]:
                cloth_item = item
                found_flag = True
                break
        if found_flag:
            break
                
    print(color,cloth_item,"detected!")

    matches = get_match([color,cloth_item])
    
    suggestions_data = []
    print("Matches:")
    for match in matches:
        print(match)

        suggestions_data.append(get_suggested_search_data(match.split(" ")))
    
    print("\nSUGGESTIONS:\n")
    for i, sugg in enumerate(suggestions_data):
        print("Suggestion #",i+1,": ",sugg[:sugg.find("product_link")])
        # for s in sugg:
        # print("title:",sugg["title"])
        # print("URL:",sugg["product_link"])
    
    return suggestions_data

# Test
# run()