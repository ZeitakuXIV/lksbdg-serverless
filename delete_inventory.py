import boto3
import os
import json

def lamda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table(os.environ['TABLE_NAME'])
    inventoryID = event['pathParameters']['id']

    try:
        response = table.delete_item(
            Key={
                'inventoryID': inventoryID
            }
        )

        return buildResponse("success", 200, None)
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