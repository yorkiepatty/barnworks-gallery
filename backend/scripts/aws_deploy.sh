#!/bin/bash
# Enhanced AWS Deployment Script for AlphaVox
# This script provides options for deploying to AWS using various methods

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DEFAULT_REGION="us-west-2"
DEFAULT_ENV="staging"
DEFAULT_METHOD="eb"

# Banner
echo -e "${BLUE}"
echo "  █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗ ██╗   ██╗ ██████╗ ██╗  ██╗"
echo " ██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══██╗╚██╗██╔╝"
echo " ███████║██║     ██████╔╝███████║███████║██║   ██║██║   ██║ ╚███╔╝ "
echo " ██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║╚██╗ ██╔╝██║   ██║ ██╔██╗ "
echo " ██║  ██║███████╗██║     ██║  ██║██║  ██║ ╚████╔╝ ╚██████╔╝██╔╝ ██╗"
echo " ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝"
echo -e "${GREEN}Enhanced AWS Deployment Script${NC}\n"

# Functions
show_help() {
    echo -e "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -h, --help            Show this help message"
    echo "  -r, --region REGION   AWS region (default: $DEFAULT_REGION)"
    echo "  -e, --env ENV         Environment: staging or production (default: $DEFAULT_ENV)"
    echo "  -m, --method METHOD   Deployment method: eb, cloudformation, or ecs (default: $DEFAULT_METHOD)"
    echo "  -p, --profile PROFILE AWS CLI profile to use"
    echo "  -v, --version VERSION Version label or Git commit hash"
    echo "  -b, --build-only      Build deployment package but don't deploy"
    echo "  -s, --skip-build      Skip build and use existing package"
    echo
}

check_prerequisites() {
    # Check AWS CLI
    echo -e "${YELLOW}Checking prerequisites...${NC}"

    if ! command -v aws &> /dev/null; then
        echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
        echo "  Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        exit 1
    fi

    # Check AWS credentials
    if [[ -n "$AWS_PROFILE" ]]; then
        profile_arg="--profile $AWS_PROFILE"
    else
        profile_arg=""
    fi

    if ! aws $profile_arg sts get-caller-identity &> /dev/null; then
        echo -e "${RED}AWS credentials not found or invalid.${NC}"
        echo "  Run 'aws configure' to set up your credentials"
        exit 1
    fi

    # Check specific prerequisites based on method
    case "$DEPLOY_METHOD" in
        eb)
            if ! command -v eb &> /dev/null; then
                echo -e "${RED}Elastic Beanstalk CLI not found.${NC}"
                echo "  Install with: pip install awsebcli"
                exit 1
            fi
            ;;
        ecs)
            ;;
        cloudformation)
            ;;
    esac

    echo -e "${GREEN}Prerequisites check passed${NC}"
}

build_package() {
    if [[ "$SKIP_BUILD" == "true" ]]; then
        echo -e "${YELLOW}Skipping build as requested${NC}"
        return
    fi

    echo -e "${YELLOW}Building deployment package...${NC}"

    # Create a temporary directory for the package
    PACKAGE_DIR=$(mktemp -d)
    ZIP_FILE="deploy.zip"

    # Copy necessary files
    echo "Copying files to package directory..."
    cp -r *.py $PACKAGE_DIR/
    cp -r models/ $PACKAGE_DIR/
    cp -r static/ $PACKAGE_DIR/
    cp -r templates/ $PACKAGE_DIR/
    cp -r routes/ $PACKAGE_DIR/
    cp -r modules/ $PACKAGE_DIR/
    cp -r scripts/ $PACKAGE_DIR/
    cp -r .ebextensions/ $PACKAGE_DIR/
    cp pyproject.toml $PACKAGE_DIR/

    if [[ "$DEPLOY_METHOD" == "eb" ]]; then
        # Create a ZIP file for Elastic Beanstalk
        echo "Creating ZIP file for Elastic Beanstalk..."
        (cd $PACKAGE_DIR && zip -r ../$ZIP_FILE *)
    elif [[ "$DEPLOY_METHOD" == "cloudformation" ]]; then
        # Create CloudFormation package
        echo "Creating CloudFormation package..."
        aws $profile_arg cloudformation package \
            --template-file cloudformation/alphavox-infrastructure.yml \
            --s3-bucket alphavox-deployments \
            --output-template-file packaged-template.yml
    elif [[ "$DEPLOY_METHOD" == "ecs" ]]; then
        # Build Docker image for ECS
        echo "Building Docker image for ECS..."
        docker build -t alphavox:latest .
    fi

    # Clean up
    rm -rf $PACKAGE_DIR

    echo -e "${GREEN}Build completed successfully${NC}"
    if [[ "$BUILD_ONLY" == "true" ]]; then
        echo -e "${YELLOW}Exiting as build-only was specified${NC}"
        exit 0
    fi
}

deploy_eb() {
    echo -e "${YELLOW}Deploying to Elastic Beanstalk...${NC}"

    # Initialize EB if needed
    if [[ ! -d .elasticbeanstalk ]]; then
        echo "Initializing Elastic Beanstalk..."
        eb init AlphaVox --region $AWS_REGION --platform "Python 3.11"
    fi

    # Deploy to the specified environment
    ENV_NAME="alphavox-$ENVIRONMENT"

    # Check if environment exists
    if ! eb status $ENV_NAME &> /dev/null; then
        echo "Environment $ENV_NAME does not exist. Creating it..."
        eb create $ENV_NAME --region $AWS_REGION --platform "Python 3.11"
    else
        echo "Deploying to existing environment $ENV_NAME..."
        eb deploy $ENV_NAME --region $AWS_REGION
    fi

    # Get the Elastic Beanstalk environment URL
    ENV_URL=$(eb status $ENV_NAME | grep CNAME | awk '{print $2}')

    echo -e "${GREEN}Deployment to Elastic Beanstalk completed successfully${NC}"
    echo -e "Application URL: ${BLUE}http://$ENV_URL${NC}"
}

deploy_cloudformation() {
    echo -e "${YELLOW}Deploying to AWS CloudFormation...${NC}"

    STACK_NAME="alphavox-$ENVIRONMENT"

    # Create or update CloudFormation stack
    if aws $profile_arg cloudformation describe-stacks --stack-name $STACK_NAME &> /dev/null; then
        echo "Updating existing CloudFormation stack $STACK_NAME..."
        aws $profile_arg cloudformation update-stack \
            --stack-name $STACK_NAME \
            --template-body file://packaged-template.yml \
            --capabilities CAPABILITY_IAM
    else
        echo "Creating new CloudFormation stack $STACK_NAME..."
        aws $profile_arg cloudformation create-stack \
            --stack-name $STACK_NAME \
            --template-body file://packaged-template.yml \
            --capabilities CAPABILITY_IAM
    fi

    echo "Waiting for stack operation to complete..."
    aws $profile_arg cloudformation wait stack-create-complete --stack-name $STACK_NAME || \
    aws $profile_arg cloudformation wait stack-update-complete --stack-name $STACK_NAME

    # Get the output value from CloudFormation stack
    APP_URL=$(aws $profile_arg cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='AlphaVoxURL'].OutputValue" --output text)

    echo -e "${GREEN}Deployment to CloudFormation completed successfully${NC}"
    echo -e "Application URL: ${BLUE}$APP_URL${NC}"
}

deploy_ecs() {
    echo -e "${YELLOW}Deploying to AWS ECS...${NC}"

    # Get AWS account ID
    AWS_ACCOUNT_ID=$(aws $profile_arg sts get-caller-identity --query Account --output text)

    # Set ECR repository URI
    ECR_REPO="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/alphavox"

    # Create ECR repository if it doesn't exist
    if ! aws $profile_arg ecr describe-repositories --repository-names alphavox &> /dev/null; then
        echo "Creating ECR repository..."
        aws $profile_arg ecr create-repository --repository-name alphavox
    fi

    # Authenticate Docker with ECR
    echo "Authenticating Docker with ECR..."
    aws $profile_arg ecr get-login-password | docker login --username AWS --password-stdin $ECR_REPO

    # Tag and push Docker image
    echo "Tagging and pushing Docker image to ECR..."
    docker tag alphavox:latest $ECR_REPO:latest
    docker push $ECR_REPO:latest

    # Update ECS task definition
    echo "Updating ECS task definition..."
    sed -e "s|ACCOUNT_ID|$AWS_ACCOUNT_ID|g" \
        -e "s|REGION|$AWS_REGION|g" \
        .aws/ecs-task-definition.json > updated-task-def.json

    # Register the task definition
    TASK_DEF_ARN=$(aws $profile_arg ecs register-task-definition --cli-input-json file://updated-task-def.json --query 'taskDefinition.taskDefinitionArn' --output text)

    # Check if ECS cluster exists
    CLUSTER_NAME="alphavox-$ENVIRONMENT"
    if ! aws $profile_arg ecs describe-clusters --clusters $CLUSTER_NAME --query 'clusters[0].status' --output text &> /dev/null; then
        echo "Creating ECS cluster $CLUSTER_NAME..."
        aws $profile_arg ecs create-cluster --cluster-name $CLUSTER_NAME
    fi

    # Check if ECS service exists
    SERVICE_NAME="alphavox-service"
    if aws $profile_arg ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --query 'services[0].status' --output text &> /dev/null; then
        echo "Updating existing ECS service..."
        aws $profile_arg ecs update-service \
            --cluster $CLUSTER_NAME \
            --service $SERVICE_NAME \
            --task-definition $TASK_DEF_ARN \
            --force-new-deployment
    else
        echo "Creating new ECS service..."
        aws $profile_arg ecs create-service \
            --cluster $CLUSTER_NAME \
            --service-name $SERVICE_NAME \
            --task-definition $TASK_DEF_ARN \
            --desired-count 1 \
            --launch-type FARGATE \
            --network-configuration "awsvpcConfiguration={subnets=[subnet-12345,subnet-67890],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
    fi

    echo -e "${GREEN}Deployment to ECS completed successfully${NC}"
    echo -e "Check the AWS console for service URL"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -r|--region)
            AWS_REGION="$2"
            shift 2
            ;;
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -m|--method)
            DEPLOY_METHOD="$2"
            shift 2
            ;;
        -p|--profile)
            AWS_PROFILE="$2"
            shift 2
            ;;
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -b|--build-only)
            BUILD_ONLY="true"
            shift
            ;;
        -s|--skip-build)
            SKIP_BUILD="true"
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Set defaults for unspecified options
AWS_REGION=${AWS_REGION:-$DEFAULT_REGION}
ENVIRONMENT=${ENVIRONMENT:-$DEFAULT_ENV}
DEPLOY_METHOD=${DEPLOY_METHOD:-$DEFAULT_METHOD}
BUILD_ONLY=${BUILD_ONLY:-"false"}
SKIP_BUILD=${SKIP_BUILD:-"false"}

if [[ "$AWS_PROFILE" ]]; then
    profile_arg="--profile $AWS_PROFILE"
else
    profile_arg=""
fi

# Display selected options
echo -e "${BLUE}Deployment Configuration:${NC}"
echo -e "  - Region:   ${YELLOW}$AWS_REGION${NC}"
echo -e "  - Environment: ${YELLOW}$ENVIRONMENT${NC}"
echo -e "  - Method:   ${YELLOW}$DEPLOY_METHOD${NC}"
if [[ "$AWS_PROFILE" ]]; then
    echo -e "  - AWS Profile: ${YELLOW}$AWS_PROFILE${NC}"
fi
echo

# Check prerequisites
check_prerequisites

# Build package
build_package

# Deploy based on method
case "$DEPLOY_METHOD" in
    eb)
        deploy_eb
        ;;
    cloudformation)
        deploy_cloudformation
        ;;
    ecs)
        deploy_ecs
        ;;
    *)
        echo -e "${RED}Unknown deployment method: $DEPLOY_METHOD${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Deployment process completed successfully${NC}"
