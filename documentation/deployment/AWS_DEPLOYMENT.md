# AlphaVox AWS Deployment Guide

This guide provides comprehensive instructions for deploying the AlphaVox application to Amazon Web Services (AWS). The deployment process includes multiple methods to fit different requirements and preferences.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Deployment Methods](#deployment-methods)
3. [Environment Configuration](#environment-configuration)
4. [Elastic Beanstalk Deployment](#elastic-beanstalk-deployment)
5. [CloudFormation Deployment](#cloudformation-deployment)
6. [ECS Deployment](#ecs-deployment)
7. [CI/CD with GitHub Actions](#ci-cd-with-github-actions)
8. [Database Configuration](#database-configuration)
9. [Secrets Management](#secrets-management)
10. [Monitoring and Logging](#monitoring-and-logging)
11. [Scaling Configuration](#scaling-configuration)
12. [Troubleshooting](#troubleshooting)
13. [Rollback Procedures](#rollback-procedures)

## Prerequisites

Before deploying AlphaVox to AWS, ensure you have the following:

- AWS account with appropriate permissions
- AWS CLI installed and configured
- Elastic Beanstalk CLI installed (if using EB deployment)
- Docker installed (if using container-based deployment)
- PostgreSQL database credentials
- API keys for OpenAI and Anthropic
- A secure secret key for session encryption

## Deployment Methods

AlphaVox can be deployed to AWS using three primary methods:

1. **Elastic Beanstalk (EB)**: Simplest method with automatic environment provisioning
2. **CloudFormation**: Infrastructure-as-Code approach for complete environment control
3. **ECS/Fargate**: Container-based deployment for improved scalability and isolation

Each method has advantages for different use cases:

| Deployment Method | Best For | Key Advantages | Complexity |
|-------------------|----------|----------------|------------|
| Elastic Beanstalk | Quick deployments, small teams | Simple, minimal configuration | Low |
| CloudFormation | Complete infrastructure, production | Full control, infrastructure as code | High |
| ECS/Fargate | Container-based, microservices | Isolation, resource efficiency | Medium |

## Environment Configuration

AlphaVox supports multiple environments:

- **Staging**: For testing before production release
- **Production**: For live application use

Environment-specific configuration is managed through:

1. Environment variables in Elastic Beanstalk
2. Parameter Store values in CloudFormation/ECS
3. Configuration files in `.ebextensions`

## Elastic Beanstalk Deployment

To deploy to Elastic Beanstalk, use the provided script:

```bash
./scripts/aws_deploy.sh --method eb --env [staging|production]
```text
This will:

1. Package the application
2. Create or update the EB environment
3. Deploy the application
4. Configure environment variables

Elastic Beanstalk configuration is provided in the `.ebextensions` directory with multiple configurations:

- `01_flask.config`: Flask application configuration
- `02_database.config`: Database connections and parameters
- `03_secrets.config`: Secure secrets management

To manually deploy:

1. Initialize EB (if not already done):

   ```bash
   eb init AlphaVox --region us-west-2 --platform "Python 3.11"
   ```

2. Create the environment (if needed):

   ```bash
   eb create alphavox-[environment] --region us-west-2
   ```

3. Deploy the application:

   ```bash
   eb deploy alphavox-[environment]
   ```

## CloudFormation Deployment

For a complete infrastructure deployment using CloudFormation:

```bash
./scripts/aws_deploy.sh --method cloudformation --env [staging|production]
```text
The CloudFormation template (`cloudformation/alphavox-infrastructure.yml`) creates:

- VPC with public and private subnets
- RDS PostgreSQL database
- Application load balancer
- ECS cluster with Fargate
- CloudFront distribution
- S3 buckets for static assets
- CloudWatch alarms
- IAM roles and policies
- Security groups

To manually deploy:

1. Create an S3 bucket for CloudFormation templates:

   ```bash
   aws s3 mb s3://alphavox-deployments
   ```

2. Package the CloudFormation template:

   ```bash
   aws cloudformation package \
     --template-file cloudformation/alphavox-infrastructure.yml \
     --s3-bucket alphavox-deployments \
     --output-template-file packaged-template.yml
   ```

3. Deploy the CloudFormation stack:

   ```bash
   aws cloudformation create-stack \
     --stack-name alphavox-[environment] \
     --template-body file://packaged-template.yml \
     --capabilities CAPABILITY_IAM \
     --parameters \
       ParameterKey=EnvironmentName,ParameterValue=[environment] \
       ParameterKey=DBUsername,ParameterValue=[username] \
       ParameterKey=DBPassword,ParameterValue=[password]
   ```

## ECS Deployment

For container-based deployment with ECS:

```bash
./scripts/aws_deploy.sh --method ecs --env [staging|production]
```text
This process:

1. Builds a Docker image using the Dockerfile
2. Pushes the image to Amazon ECR
3. Updates the ECS task definition
4. Deploys the new service

The ECS task definition is available at `.aws/ecs-task-definition.json`.

To manually deploy:

1. Authenticate Docker with ECR:

   ```bash
   aws ecr get-login-password | docker login --username AWS --password-stdin [account-id].dkr.ecr.[region].amazonaws.com
   ```

2. Build and push the Docker image:

   ```bash
   docker build -t [account-id].dkr.ecr.[region].amazonaws.com/alphavox:latest .
   docker push [account-id].dkr.ecr.[region].amazonaws.com/alphavox:latest
   ```

3. Update the ECS service:

   ```bash
   aws ecs update-service \
     --cluster alphavox-[environment] \
     --service alphavox-service \
     --force-new-deployment
   ```

## CI/CD with GitHub Actions

AlphaVox includes GitHub Actions workflows for automatic deployment:

- On push to `main` branch: Deploys to production
- On push to `develop` branch: Deploys to staging
- Manual workflow dispatch: Deploys to specified environment

The workflow configuration is in `.github/workflows/deploy.yml`.

To use GitHub Actions:

1. Add the following secrets to your GitHub repository:

   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `DATABASE_URL`
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `SESSION_SECRET`

2. Push to the appropriate branch or use the manual workflow dispatch.

## Database Configuration

AlphaVox requires a PostgreSQL database, which can be configured in multiple ways:

1. **RDS Instance** (recommended for production):

   - Created automatically by CloudFormation
   - Manual creation through AWS console
   - Connection string stored in environment variables or Parameter Store

2. **External Database**:

   - Update the `DATABASE_URL` environment variable to point to your database

Database migrations are handled through the deployment process:

- For Elastic Beanstalk: Container commands in `.ebextensions/02_database.config`
- For ECS/CloudFormation: Post-deployment tasks in the CI/CD workflow

## Secrets Management

AlphaVox requires several secrets for operation:

1. `DATABASE_URL`: PostgreSQL connection string
2. `OPENAI_API_KEY`: OpenAI API key
3. `ANTHROPIC_API_KEY`: Anthropic API key
4. `SESSION_SECRET`: Secret key for session management

These secrets are managed securely through:

- **Elastic Beanstalk**: Environment properties with encryption
- **CloudFormation/ECS**: AWS Systems Manager Parameter Store

Never store secrets in code or commit them to the repository.

To set up secrets in Parameter Store:

```bash
aws ssm put-parameter \
  --name /alphavox/DATABASE_URL \
  --value "your-connection-string" \
  --type SecureString

aws ssm put-parameter \
  --name /alphavox/OPENAI_API_KEY \
  --value "your-api-key" \
  --type SecureString

aws ssm put-parameter \
  --name /alphavox/ANTHROPIC_API_KEY \
  --value "your-api-key" \
  --type SecureString

aws ssm put-parameter \
  --name /alphavox/SESSION_SECRET \
  --value "your-secret-key" \
  --type SecureString
```text
## Monitoring and Logging

AlphaVox is configured with comprehensive monitoring and logging:

1. **CloudWatch Logs**:

   - Application logs
   - Access logs
   - Error logs

2. **CloudWatch Metrics**:

   - CPU and memory utilization
   - Request count and latency
   - Error rates

3. **CloudWatch Alarms**:

   - High CPU usage
   - High memory usage
   - Unhealthy hosts
   - 5xx error rate

4. **Health Checks**:

   - `/health` endpoint for basic health checks
   - `/health/detailed` for detailed status

To view logs:

```bash

# For Elastic Beanstalk

eb logs alphavox-[environment]

# For ECS

aws logs get-log-events \
  --log-group-name /ecs/alphavox-[environment] \
  --log-stream-name [log-stream-name]
```text
## Scaling Configuration

AlphaVox supports automatic scaling based on load:

1. **Elastic Beanstalk**:

   - Auto Scaling configured in `.ebextensions/01_flask.config`
   - Scales based on CPU utilization

2. **ECS**:

   - Service Auto Scaling in CloudFormation template
   - Scales based on CPU and memory utilization

3. **RDS**:

   - Auto scaling storage in CloudFormation template

To modify scaling settings:

- For Elastic Beanstalk: Update `.ebextensions/01_flask.config`
- For ECS/CloudFormation: Update the CloudFormation template and redeploy

## Troubleshooting

Common issues and their solutions:

1. **Deployment Failure**:

   - Check the deployment logs:
     ```bash
     eb logs alphavox-[environment]
     ```
   - Verify AWS credentials and permissions

2. **Application Errors**:

   - Check the application logs:
     ```bash
     eb logs alphavox-[environment] --all
     ```
   - Verify environment variables are set correctly

3. **Database Connection Issues**:

   - Confirm the database exists and is accessible
   - Check security group rules allow access from the application
   - Verify the `DATABASE_URL` secret is correctly formatted

4. **Health Check Failures**:

   - Ensure the application is running and the `/health` endpoint is accessible
   - Check for errors in the application logs

5. **Container Issues (ECS)**:

   - Check the container logs in CloudWatch
   - Verify the task definition is correct
   - Check the container can access required secrets

## Rollback Procedures

If a deployment fails or causes issues:

1. **Elastic Beanstalk Rollback**:

   ```bash
   eb rollback alphavox-[environment]
   ```

2. **CloudFormation Rollback**:

   ```bash
   aws cloudformation rollback-stack \
     --stack-name alphavox-[environment]
   ```

3. **ECS Rollback**:

   ```bash
   aws ecs update-service \
     --cluster alphavox-[environment] \
     --service alphavox-service \
     --task-definition [previous-task-definition]
   ```

4. **Database Rollback**:

   Restore from the most recent automated backup in RDS:
   ```bash
   aws rds restore-db-instance-to-point-in-time \
     --source-db-instance-identifier alphavox-[environment]-database \
     --target-db-instance-identifier alphavox-[environment]-database-restored \
     --restore-time [timestamp]
   ```

## Additional Resources

- [AWS Elastic Beanstalk Documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)
- [AWS CloudFormation Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [AWS ECS Documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
