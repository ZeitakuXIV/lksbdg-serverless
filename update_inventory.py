import boto3
import os
from datetime import datetime
import json

def lambda_handler(event, context):

    client = boto3.resource('dynamodb')
    table = client.Table(os.environ['TABLE_NAME'])

    try:
        inventoryID = event['pathParameters']['id']
        request = json.loads(event['body'])
        response = table.update_item(
            Key={
                'inventoryID': inventoryID
            },
            UpdateExpression="set inventoryStatus = :inventoryStatus, lastUpdatedAt = :lastUpdatedAt",
            ExpressionAttributeValues={
                ':inventoryStatus': request['inventoryStatus'],
                ':lastUpdatedAt': datetime.now().isoformat()
            },
            ReturnValues="UPDATED_NEW"
        )

        return buildResponse("success", 200, response['Attributes'])
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