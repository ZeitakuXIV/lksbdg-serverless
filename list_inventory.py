import boto3
import os
import json
from datetime import datetime

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table(os.environ['TABLE_NAME'])

    try:
        response = table.scan()
        
        return buildResponse("success", 200, response['Items'])
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