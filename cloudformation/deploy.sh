#!/bin/bash -e

NETWORK="00-network"
security_groups="01-securityGroups"
aurora="02-aurora"
s3processor="03-SAMs3processor"
kinesis="04-kinesis"
kinesisCollector="05-SAMkinesisCollector"
continuousIntegration="06-continuousIntegration"
bucketName=$1
stackName=$2

mkdir -p ../src/modules
pip install -r ../src/requirements.txt -t ../src/modules

aws cloudformation package --template-file "$NETWORK.yml" \
            --s3-bucket $bucketName \
            --output-template-file $NETWORK.packaged.yml

aws cloudformation package --template-file "$security_groups.yml" \
            --s3-bucket $bucketName \
            --output-template-file $security_groups.packaged.yml

aws cloudformation package --template-file "$aurora.yml" \
            --s3-bucket $bucketName \
            --output-template-file $aurora.packaged.yml

aws cloudformation package --template-file "$s3processor.yml" \
            --s3-bucket $bucketName \
            --output-template-file $s3processor.packaged.yml

aws cloudformation package --template-file "$kinesis.yml" \
            --s3-bucket $bucketName \
            --output-template-file $kinesis.packaged.yml

aws cloudformation package --template-file "$kinesisCollector.yml" \
            --s3-bucket $bucketName \
            --output-template-file $kinesisCollector.packaged.yml

aws cloudformation package --template-file "$continuousIntegration.yml" \
            --s3-bucket $bucketName \
            --output-template-file $continuousIntegration.packaged.yml

aws s3api put-object --bucket $bucketName --body $NETWORK.packaged.yml --key $NETWORK.packaged.yml
aws s3api put-object --bucket $bucketName --body $security_groups.packaged.yml --key $security_groups.packaged.yml
aws s3api put-object --bucket $bucketName --body $aurora.packaged.yml --key $aurora.packaged.yml
aws s3api put-object --bucket $bucketName --body $s3processor.packaged.yml --key $s3processor.packaged.yml
aws s3api put-object --bucket $bucketName --body $kinesis.packaged.yml --key $kinesis.packaged.yml
aws s3api put-object --bucket $bucketName --body $kinesisCollector.packaged.yml --key $kinesisCollector.packaged.yml
aws s3api put-object --bucket $bucketName --body $continuousIntegration.packaged.yml --key $continuousIntegration.packaged.yml

if [ "$3" = "push" ]
then
    aws cloudformation deploy --template-file overstack.yml --parameter-overrides BucketName=$bucketName StackName=$stackName --stack-name $stackName --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
fi

rm -rf *packaged*.yml
rm -rf /src/modules
