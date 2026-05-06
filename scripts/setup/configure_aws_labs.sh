#!/bin/bash

set -e

CREDENTIALS_FILE="aws_labs_credentials.txt"
PROFILE_NAME="default"

if [ ! -f "$CREDENTIALS_FILE" ]; then
  echo "No existe $CREDENTIALS_FILE"
  echo "Pega ahí las credenciales temporales de AWS Learner Labs."
  exit 1
fi

source "$CREDENTIALS_FILE"

aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID" --profile "$PROFILE_NAME"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY" --profile "$PROFILE_NAME"
aws configure set aws_session_token "$AWS_SESSION_TOKEN" --profile "$PROFILE_NAME"
aws configure set region "${AWS_DEFAULT_REGION:-us-east-1}" --profile "$PROFILE_NAME"

echo "Credenciales configuradas en el perfil: $PROFILE_NAME"
aws sts get-caller-identity --profile "$PROFILE_NAME"