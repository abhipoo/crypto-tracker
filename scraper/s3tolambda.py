import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("Key: " + str(key))
        #print("File content type: " + str(type(response["Body"])))
        print("Response body into string: ")
        object_as_string = response["Body"].read().decode('utf-8')
        print(object_as_string)
        json_obj = json.loads(object_as_string)
        print("json: ")
        print(json_obj)
        #print("CONTENT TYPE: " + response['ContentType'])
        #return response['ContentType']
        
        #insert data to dynamodb
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('cryptocurrency')
        
        response = table.put_item(Item = json_obj)
        print("Insert operation successful")

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
