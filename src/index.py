""" Kinesis Firehose Processing Logic """
import json
import boto3
import os
import sys

sys.path.append("modules")
import pymysql.cursors
import requests

from sqlalchemy.schema import CreateSchema
from sqlalchemy import Column, String, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sample(Base):
    __tablename__ = 'samples'
    timestamp = Column(Numeric, primary_key=True)
    value = Column(String, primary_key=True)
    device_id = Column(String, primary_key=True)
    data = Column(Numeric)


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
        engine = create_engine('mysql+pymysql://' +
                               os.environ.get('DB_USERNAME') +
                               ':' +
                               os.environ.get('DB_PASSWORD') +
                               '@' +
                               os.environ.get('DB_ENDPOINT') +
                               ':' +
                               os.environ.get('DB_PORT') +
                               '/' +
                               os.environ.get('DB_NAME'))
        engine.execute(CreateSchema('my_schema'))

    finally:
        print("foo")
    print("doing a thing")
    # Connect to the database
    for record in event['Records']:
        print(record['s3']['object']['key'])
