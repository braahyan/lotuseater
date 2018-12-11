""" Kinesis Firehose Processing Logic """
import json
import boto3
import os
import sys

sys.path.append("modules")
import pymysql.cursors
import requests


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
        connection = pymysql.connect(host=os.environ.get('AURORA_ENDPOINT'),
                                     user=os.environ.get('DATABASE_USERNAME'),
                                     password=os.environ.get('DATABASE_PASSWORD'),
                                     db=os.environ.get('DATABASE_NAME'),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT now()"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
    print("doing a thing")
    # Connect to the database
    for record in event['Records']:
        print(record['s3']['object']['key'])
