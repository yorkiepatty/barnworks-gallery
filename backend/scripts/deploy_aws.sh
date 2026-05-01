#!/bin/bash

# AWS Elastic Beanstalk deployment script for AlphaVox
# This script prepares and deploys the application to AWS Elastic Beanstalk

# Configuration - Update these values
APP_NAME="alphavox"
ENV_NAME="alphavox-production"
AWS_REGION="us-west-2"  # Change to your preferred region
S3_BUCKET="alphavox-deployments"  # S3 bucket to store deployment packages

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting AlphaVox AWS Deployment${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    echo "Follow instructions at: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check if AWS EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo -e "${RED}AWS Elastic Beanstalk CLI is not installed. Please install it first.${NC}"
    echo "Run: pip install awsebcli"
    exit 1
fi

# Verify AWS credentials
echo -e "${YELLOW}Verifying AWS credentials...${NC}"
aws sts get-caller-identity &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}AWS credentials not configured or invalid.${NC}"
    echo "Run: aws configure"
    exit 1
fi

# Create deployment package
echo -e "${YELLOW}Creating deployment package...${NC}"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
ZIP_FILE="alphavox-$TIMESTAMP.zip"

# Create a version file
echo "AlphaVox deployment version: $TIMESTAMP" > version.txt

# Create zip file with all necessary files
zip -r "$ZIP_FILE" . -x "*.git*" "*.zip" "*.pyc" "__pycache__/*" "venv/*" "*.DS_Store" "deploy_aws.sh"

# Create S3 bucket if it doesn't exist
aws s3api head-bucket --bucket "$S3_BUCKET" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Creating S3 bucket for deployments...${NC}"
    aws s3 mb "s3://$S3_BUCKET" --region "$AWS_REGION"
fi

# Upload deployment package to S3
echo -e "${YELLOW}Uploading deployment package to S3...${NC}"
aws s3 cp "$ZIP_FILE" "s3://$S3_BUCKET/"

# Check if application exists
aws elasticbeanstalk describe-applications --application-names "$APP_NAME" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Creating Elastic Beanstalk application...${NC}"
    aws elasticbeanstalk create-application --application-name "$APP_NAME" --region "$AWS_REGION"
fi

# Check if environment exists
aws elasticbeanstalk describe-environments --application-name "$APP_NAME" --environment-names "$ENV_NAME" &> /dev/null
ENV_EXISTS=$?

# Create application version
echo -e "${YELLOW}Creating application version...${NC}"
aws elasticbeanstalk create-application-version \
    --application-name "$APP_NAME" \
    --version-label "v-$TIMESTAMP" \
    --source-bundle S3Bucket="$S3_BUCKET",S3Key="$ZIP_FILE" \
    --region "$AWS_REGION"

if [ $ENV_EXISTS -ne 0 ]; then
    # Create environment if it doesn't exist
    echo -e "${YELLOW}Creating Elastic Beanstalk environment...${NC}"
    aws elasticbeanstalk create-environment \
        --application-name "$APP_NAME" \
        --environment-name "$ENV_NAME" \
        --solution-stack-name "64bit Amazon Linux 2023 v4.0.0 running Python 3.11" \
        --version-label "v-$TIMESTAMP" \
        --region "$AWS_REGION"
else
    # Update existing environment
    echo -e "${YELLOW}Updating Elastic Beanstalk environment...${NC}"
    aws elasticbeanstalk update-environment \
        --application-name "$APP_NAME" \
        --environment-name "$ENV_NAME" \
        --version-label "v-$TIMESTAMP" \
        --region "$AWS_REGION"
fi

# Clean up local zip file
rm "$ZIP_FILE"
rm "version.txt"

echo -e "${GREEN}Deployment in progress! You can check the status in the AWS Elastic Beanstalk Console.${NC}"
echo -e "${GREEN}Once deployment completes, the application will be available at:${NC}"
echo -e "${GREEN}http://$ENV_NAME.elasticbeanstalk.com${NC}"

exit 0
