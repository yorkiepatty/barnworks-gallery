#!/bin/bash
# AWS Deployment Test Script for AlphaVox
# This script validates that all necessary prerequisites for AWS deployment are met

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}AlphaVox AWS Deployment Validation${NC}"
echo "Running pre-deployment validation checks..."
echo

# Initialize success counters
TOTAL_CHECKS=0
PASSED_CHECKS=0

# Function to run a check
run_check() {
    local name=$1
    local command=$2

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    echo -ne "${YELLOW}[ RUNNING ]${NC} $name... "

    # Run the command and capture output
    local output
    if output=$(eval "$command" 2>&1); then
        echo -e "\r${GREEN}[  PASSED  ]${NC} $name"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "\r${RED}[  FAILED  ]${NC} $name"
        echo
        echo -e "${RED}Error output:${NC}"
        echo "$output" | sed 's/^/  /'
        echo
    fi
}

# Check AWS CLI installation
run_check "AWS CLI Installation" "command -v aws &> /dev/null"

# Check AWS credentials
run_check "AWS Credentials" "aws sts get-caller-identity &> /dev/null"

# Check EB CLI installation
run_check "Elastic Beanstalk CLI Installation" "command -v eb &> /dev/null || echo 'EB CLI not installed but can be skipped if not deploying to Elastic Beanstalk'"

# Check Docker installation
run_check "Docker Installation" "command -v docker &> /dev/null || echo 'Docker not installed but can be skipped if not deploying containers'"

# Check required files for Elastic Beanstalk
run_check "Elastic Beanstalk Files" "test -d .ebextensions && test -f main.py"

# Check Dockerfile
run_check "Dockerfile" "test -f Dockerfile"

# Check CloudFormation template
run_check "CloudFormation Template" "test -f cloudformation/alphavox-infrastructure.yml"

# Check Python version
run_check "Python Version" "python -c 'import sys; exit(0 if sys.version_info >= (3,11) else 1)'"

# Check PostgreSQL client
run_check "PostgreSQL Client" "command -v psql &> /dev/null || pip show psycopg2-binary &> /dev/null"

# Check package installation
run_check "Python Packages" "pip show flask gunicorn &> /dev/null"

# Check deployment scripts
run_check "Deployment Scripts" "test -f scripts/aws_deploy.sh && test -x scripts/aws_deploy.sh"

# Check required environment variables
run_check "Environment Variables" "[[ -n \$DATABASE_URL || -n \$OPENAI_API_KEY || -n \$ANTHROPIC_API_KEY ]] || echo 'Some environment variables may be missing but can be set during deployment'"

# Check application health endpoint
run_check "Health Endpoint" "curl -s http://localhost:5000/health &> /dev/null || echo 'Application not running locally, skipping health check'"

# Print summary
echo
echo -e "${BLUE}Validation Summary:${NC}"
echo -e "Passed ${GREEN}$PASSED_CHECKS${NC} out of ${YELLOW}$TOTAL_CHECKS${NC} checks"

if [[ $PASSED_CHECKS -eq $TOTAL_CHECKS ]]; then
    echo -e "${GREEN}All checks passed. Your application is ready for AWS deployment!${NC}"
    exit 0
else
    PERCENT=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
    if [[ $PERCENT -ge 80 ]]; then
        echo -e "${YELLOW}Most checks passed ($PERCENT%). Review failures before deployment.${NC}"
        exit 1
    else
        echo -e "${RED}Only $PERCENT% of checks passed. Please fix the issues before deployment.${NC}"
        exit 2
    fi
fi
