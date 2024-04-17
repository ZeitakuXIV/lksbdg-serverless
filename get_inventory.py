import boto3
import os
import json

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table(os.environ['TABLE_NAME'])

    try:
        response = table.get_item(
            Key={
                'inventoryID': event['pathParameters']['id']
            }
        )
        
        if 'Item' in response:
            return buildResponse("success", 200, response['Item'])
        else:
            return buildResponse("there is no matching inventoryID", 400, None)
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