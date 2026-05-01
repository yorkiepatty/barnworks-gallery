#!/bin/bash
# Script to build and deploy AlphaVox Docker image to AWS ECR

# Configuration
AWS_REGION="us-west-2"  # Change to your preferred region
ECR_REPOSITORY_NAME="alphavox"
IMAGE_TAG="latest"

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install it first.${NC}"
    exit 1
fi

# Get AWS account ID
echo -e "${YELLOW}Retrieving AWS account ID...${NC}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to get AWS account ID. Please check your AWS credentials.${NC}"
    exit 1
fi

echo -e "${GREEN}AWS Account ID: $AWS_ACCOUNT_ID${NC}"

# Set the ECR repository URI
ECR_REPOSITORY_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME"

# Check if repository exists, create it if it doesn't
echo -e "${YELLOW}Checking if ECR repository exists...${NC}"
if ! aws ecr describe-repositories --repository-names $ECR_REPOSITORY_NAME --region $AWS_REGION &> /dev/null; then
    echo -e "${YELLOW}Repository does not exist. Creating repository...${NC}"
    aws ecr create-repository --repository-name $ECR_REPOSITORY_NAME --region $AWS_REGION

    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create ECR repository.${NC}"
        exit 1
    fi

    echo -e "${GREEN}ECR repository created successfully.${NC}"
else
    echo -e "${GREEN}ECR repository already exists.${NC}"
fi

# Authenticate Docker to ECR
echo -e "${YELLOW}Authenticating Docker with ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY_URI

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to authenticate Docker with ECR.${NC}"
    exit 1
fi

echo -e "${GREEN}Authentication successful.${NC}"

# Build Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t $ECR_REPOSITORY_NAME:$IMAGE_TAG .

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to build Docker image.${NC}"
    exit 1
fi

echo -e "${GREEN}Docker image built successfully.${NC}"

# Tag the image
echo -e "${YELLOW}Tagging Docker image for ECR...${NC}"
docker tag $ECR_REPOSITORY_NAME:$IMAGE_TAG $ECR_REPOSITORY_URI:$IMAGE_TAG

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to tag Docker image.${NC}"
    exit 1
fi

echo -e "${GREEN}Docker image tagged successfully.${NC}"

# Push the image to ECR
echo -e "${YELLOW}Pushing Docker image to ECR...${NC}"
docker push $ECR_REPOSITORY_URI:$IMAGE_TAG

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to push Docker image to ECR.${NC}"
    exit 1
fi

echo -e "${GREEN}Docker image pushed successfully to ECR.${NC}"
echo -e "${GREEN}Image URI: $ECR_REPOSITORY_URI:$IMAGE_TAG${NC}"

# Update ECS task definition (if ECS is being used)
echo -e "${YELLOW}Do you want to update the ECS task definition? (y/n)${NC}"
read update_ecs

if [[ $update_ecs == "y" || $update_ecs == "Y" ]]; then
    echo -e "${YELLOW}Updating ECS task definition...${NC}"

    # Create a new task definition file with the updated image URI
    TASK_DEF_FILE=".aws/ecs-task-definition.json"
    TEMP_TASK_DEF_FILE=".aws/ecs-task-definition-updated.json"

    # Replace placeholder values in the task definition
    sed -e "s|ACCOUNT_ID|$AWS_ACCOUNT_ID|g" \
        -e "s|REGION|$AWS_REGION|g" \
        $TASK_DEF_FILE > $TEMP_TASK_DEF_FILE

    # Register the updated task definition
    NEW_TASK_DEF=$(aws ecs register-task-definition --cli-input-json file://$TEMP_TASK_DEF_FILE --region $AWS_REGION)

    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to update ECS task definition.${NC}"
        exit 1
    fi

    NEW_TASK_DEF_ARN=$(echo $NEW_TASK_DEF | jq -r '.taskDefinition.taskDefinitionArn')
    echo -e "${GREEN}ECS task definition updated successfully.${NC}"
    echo -e "${GREEN}New task definition ARN: $NEW_TASK_DEF_ARN${NC}"

    # Ask if user wants to update the ECS service
    echo -e "${YELLOW}Do you want to update an ECS service with the new task definition? (y/n)${NC}"
    read update_service

    if [[ $update_service == "y" || $update_service == "Y" ]]; then
        echo -e "${YELLOW}Enter the ECS cluster name:${NC}"
        read cluster_name

        echo -e "${YELLOW}Enter the ECS service name:${NC}"
        read service_name

        echo -e "${YELLOW}Updating ECS service...${NC}"
        aws ecs update-service --cluster $cluster_name --service $service_name \
            --task-definition $(echo $NEW_TASK_DEF_ARN | awk -F/ '{print $2}') \
            --region $AWS_REGION

        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to update ECS service.${NC}"
            exit 1
        fi

        echo -e "${GREEN}ECS service updated successfully.${NC}"
    fi
fi

echo -e "${GREEN}Deployment to AWS ECR completed successfully.${NC}"
