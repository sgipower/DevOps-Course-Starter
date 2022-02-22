#!/bin/bash -e
terraform init
terraform apply -var="APP-PREFIX=$PRODUCTION_ENV_PREFIX" -var="CLIENTID=$CLIENT_ID" -var="CLIENTSECRET=$CLIENTSECRET"  -auto-approve
curl -dH -X POST --fail "$(terraform output -raw cd_webhook)"