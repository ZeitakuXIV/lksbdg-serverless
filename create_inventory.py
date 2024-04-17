import boto3
import os
import uuid
from datetime import datetime
import json
from base64 import b64decode

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    s3_client = boto3.resource('s3')
    table = client.Table(os.environ['TABLE_NAME'])
    bucket_name = os.environ['BUCKET_NAME']


    try:
        request = json.loads(event['body'])
        image_data = request['image']
        decoded_data = b64decode(image_data)

        filename = f"{os.urandom(16).hex()}.jpg"

        s3_client.Object(bucket_name, filename).put(Body=decoded_data)

        url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"

        inventoryID = str(uuid.uuid4())
        response = table.put_item(
            Item={
                'inventoryID': inventoryID,
                'class': request['class'],
                'name': request['name'],
                'image': url,
                'inventoryStatus': request['inventoryStatus'] if request.get('inventoryStatus') else 'Available',
                'createdAt': datetime.now().isoformat(),
                'lastUpdatedAt': datetime.now().isoformat(),
            },
            ReturnValues= 'ALL_OLD'
        )

        return buildResponse("success", 200, {
            "inventoryID:": inventoryID,
            "image": url
            })
    except Exception as e:
        return buildResponse(str(e), 500, None)

def buildResponse(message, statusCode, body):
    return {
        "isBase64Encoded": False,
        "statusCode": statusCode,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps({
            "statusCode": statusCode,
            "message": message,
            "body": body
        }),
    }