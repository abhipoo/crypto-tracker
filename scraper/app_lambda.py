import json
from scrapers import coinmarketcap as cm
import datetime
import boto3
import time

def lambda_handler(event, context):
    #read config
    with open('config.json') as json_file:
        request_data = json.load(json_file)
        #print(request_data)
        data_dict = {}
        data_arr = []

        data_dict["timestamp_str"] = str(datetime.datetime.now())
        data_dict["timestamp_int"] = int(time.time())

        for record in request_data:
            #print(record["url"])
            response = cm.fetch(record["url"])
            response["currency"] = record["currency"]
            data_arr.append(response)
            print(response)

        data_dict["response"] = data_arr

    # Convert data to json
    data = json.dumps(data_dict)

    # Export the data to S3
    client = boto3.client('s3')
    
    response = client.put_object(Bucket='crypto-prices-bucket', 
                    Body=data, 
                    Key='response_{}.json'.format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))


