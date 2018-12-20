import sys
import os
sys.path.append(os.path.dirname(__file__) + "/../modules")
import json
import boto3
import requests
from models.sample import Base




def handler(event, context):
    """ Lambda entrypoint """
    print("Event: %s" % event)
    client = boto3.client('firehose')
    if 'body' in event and event['body']:
        records = json.loads(event['body'])
        print(records)
        response = client.put_record_batch(
            DeliveryStreamName=os.environ.get("STREAM_NAME"),
            Records=list(map(lambda x: {'Data': json.dumps(x) + "\n"}))

        )
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps({'records': records})
        }
    else:
        return {
            'statusCode': 200,
            'body': 'require records'
        }


# Help function to generate an IAM policy
def policy(principalId, effect, resource):
    # Required output:
    authResponse = {}
    authResponse['principalId'] = principalId
    if (effect and resource):
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'  # default version
        policyDocument['Statement'] = []
        statementOne = {}
        statementOne['Action'] = 'execute-api:Invoke'  # default action
        statementOne['Effect'] = effect
        statementOne['Resource'] = resource
        policyDocument['Statement'] = [statementOne]
        authResponse['policyDocument'] = policyDocument

    # Optional output with custom properties of the String, Number or Boolean type.
    authResponse['context'] = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": True
    }
    return authResponse


def policy_handler(event, context):
    """ Lambda entrypoint """
    print("Event: %s" % event)
    return policy('me', 'Allow', '*')


def s3_handler(event, context):
    print("Opening db connection")
    print(requests.get("https://thrivehive.com"))
    try:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(
            SecretId=os.environ.get('DB_CREDENTIALS')
        )
        creds = json.loads(response['SecretString'])


    finally:
        print("foo")
    print("doing a thing")
    # Connect to the database
    for record in event['Records']:
        print(record['s3']['object']['key'])
