#!/bin/bash -e

NETWORK="00-network"
security_groups="01-securityGroups"
aurora="02-aurora"
s3processor="03-s3processor"
kinesis="04-kinesis"
kinesisCollector="05-kinesisCollector"
continuousIntegration="06-continuousIntegration"

mkdir -p ../src/modules
if [[ $1 = "package" ]]; then
    pip install -r ../src/requirements.txt -t ../src/modules
fi

sam deploy --template-file "$NETWORK.yml" \
           --stack-name "A$NETWORK" \
           --no-fail-on-empty-changeset

sam deploy --template-file "$security_groups.yml" \
           --stack-name "A$security_groups" \
           --parameter-overrides NetworkStackName="A$NETWORK" \
           --no-fail-on-empty-changeset

sam deploy --template-file "$aurora.yml" \
           --stack-name "A$aurora" \
           --parameter-overrides NetworkStackName="A$NETWORK" \
                                 SecurityGroupStackName=A"$security_groups" \
           --no-fail-on-empty-changeset

sam package --template-file "$s3processor.yml" \
            --s3-bucket bryanpedlar-dev \
            --output-template-file packaged.yaml
sam deploy --template-file ./packaged.yaml \
           --stack-name "A$s3processor" \
           --capabilities CAPABILITY_IAM \
           --no-fail-on-empty-changeset \
           --parameter-overrides NetworkStackName="A$NETWORK" \
                                 SecurityGroupStackName=A"$security_groups" \
                                 DBStackName="A$aurora"
rm -rf packaged.yaml

sam deploy --template-file "$kinesis.yml" \
           --stack-name "A$kinesis" \
           --capabilities CAPABILITY_IAM \
           --no-fail-on-empty-changeset \
           --parameter-overrides S3ProcessorStackName="A$s3processor"

sam package --template-file "$kinesisCollector.yml" \
            --s3-bucket bryanpedlar-dev \
            --output-template-file packaged.yaml
sam deploy --template-file ./packaged.yaml \
           --stack-name "A$kinesisCollector" \
           --capabilities CAPABILITY_IAM \
           --no-fail-on-empty-changeset \
           --parameter-overrides KinesisStreamStackName="A$kinesis"

sam deploy --template-file "$continuousIntegration.yml" \
           --stack-name "A$continuousIntegration" \
           --capabilities CAPABILITY_IAM \
           --no-fail-on-empty-changeset

rm -rf packaged.yaml

rm -rf /src/modules