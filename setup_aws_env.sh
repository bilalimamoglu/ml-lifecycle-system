#!/bin/bash

# Define the project AWS directory
PROJECT_AWS_DIR=$(pwd)/.aws

# Check if the project .aws directory exists, create it if not
if [ ! -d "$PROJECT_AWS_DIR" ]; then
  mkdir -p "$PROJECT_AWS_DIR"
fi

# Copy credentials and config from $HOME/.aws to the project .aws folder
if [ -f "$HOME/.aws/credentials" ]; then
  cp "$HOME/.aws/credentials" "$PROJECT_AWS_DIR/credentials"
  echo "Copied AWS credentials to project .aws directory."
else
  echo "AWS credentials not found in $HOME/.aws/credentials. Please check."
  exit 1
fi

if [ -f "$HOME/.aws/config" ]; then
  cp "$HOME/.aws/config" "$PROJECT_AWS_DIR/config"
  echo "Copied AWS config to project .aws directory."
else
  echo "AWS config not found in $HOME/.aws/config. Please check."
  exit 1
fi

# Set environment variables to use the local AWS credentials and config
export AWS_SHARED_CREDENTIALS_FILE="$PROJECT_AWS_DIR/credentials"
export AWS_CONFIG_FILE="$PROJECT_AWS_DIR/config"

# Confirm environment variables are set
echo "AWS_SHARED_CREDENTIALS_FILE is set to $AWS_SHARED_CREDENTIALS_FILE"
echo "AWS_CONFIG_FILE is set to $AWS_CONFIG_FILE"
