#!/bin/bash -e

continuousIntegration="06-continuousIntegration"

python tropo.py
sam deploy --template-file "$continuousIntegration.yml" \
           --stack-name "A$continuousIntegration" \
           --capabilities CAPABILITY_NAMED_IAM  \
           --no-fail-on-empty-changeset \
           --parameter-overrides NotificationEmail="pedlar.bryan@gmail.com" \
                                 RepoOwner="braahyan" \
                                 RepoName="lotuseater" \
                                 RepoBranchName="master"

