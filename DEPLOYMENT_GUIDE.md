# 🚀 Deployment Guide - Repeatable IaC

## 🌍 Region & Account Strategy

**Fixed Region**: `us-east-1` (for consistency and AgentCore availability)
**Multi-Account Ready**: Deploy to any AWS account with single command

## 📋 Prerequisites

### AWS Account Setup
```bash
# Configure AWS credentials for target account
aws configure --profile target-account
export AWS_PROFILE=target-account
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Verify account and region
aws sts get-caller-identity
aws configure get region  # Should be us-east-1
```

### CDK Bootstrap (One-time per account)
```bash
# Bootstrap CDK in target account
cdk bootstrap aws://$AWS_ACCOUNT_ID/us-east-1

# Verify bootstrap
aws cloudformation describe-stacks --stack-name CDKToolkit --region us-east-1
```

## 🏗️ Deployment Commands

### Quick Deploy to Any Account
```bash
# Set target account
export AWS_ACCOUNT_ID=123456789012  # Your target account ID

# Deploy to development environment
npm run deploy:dev

# Deploy to staging environment  
npm run deploy:staging

# Deploy to production environment
npm run deploy:prod

# Deploy with specific account context
npm run deploy:account
```

### Environment-Specific Deployments
```bash
# Development (7-day retention, debug logging)
npm run deploy:dev

# Staging (14-day retention, info logging, no auto-destroy)
npm run deploy:staging

# Production (30-day retention, info logging, no auto-destroy)
npm run deploy:prod
```

## 🗑️ Clean Removal

### Complete Stack Removal
```bash
# Remove development environment
npm run destroy:dev

# Remove staging environment
npm run destroy:staging

# Remove production environment (careful!)
npm run destroy:prod

# Remove all stacks (nuclear option)
npm run destroy
```

### Verify Removal
```bash
# Check no stacks remain
aws cloudformation list-stacks --region us-east-1 --query 'StackSummaries[?contains(StackName, `SecurityChatbot`) && StackStatus != `DELETE_COMPLETE`]'

# Check no AgentCore resources remain
agentcore status
```

## 📊 Stack Structure

### Deployed Stacks (per environment)
```
SecurityChatbot-{env}-Security     # IAM roles, Cognito, security
SecurityChatbot-{env}-AgentCore    # Memory, Gateway, Runtime  
SecurityChatbot-{env}-Monitoring   # CloudWatch, alarms, dashboards
```

### Resource Naming Convention
```
security-chatbot-{env}-{resource-type}-{unique-id}

Examples:
- security-chatbot-dev-memory-abc123
- security-chatbot-prod-gateway-def456
- security-chatbot-staging-runtime-ghi789
```

## 🔄 Cross-Account Migration

### Export from Source Account
```bash
# Export configuration (if needed)
aws ssm get-parameters-by-path --path "/security-chatbot/" --region us-east-1

# Export any custom configurations
cdk synth > infrastructure-template.yaml
```

### Import to Target Account
```bash
# Switch to target account
export AWS_PROFILE=target-account
export AWS_ACCOUNT_ID=987654321098

# Bootstrap if needed
cdk bootstrap aws://$AWS_ACCOUNT_ID/us-east-1

# Deploy to target account
npm run deploy:prod
```

## 🏷️ Resource Tagging

All resources automatically tagged with:
```yaml
Project: aws-security-agentcore-chatbot
Environment: development|staging|production
Region: us-east-1
Owner: security-team
CostCenter: security-operations
ManagedBy: CDK
Repository: aws-security-agentcore-chatbot
```

## 🔍 Verification Commands

### Post-Deployment Verification
```bash
# Verify stacks deployed
aws cloudformation list-stacks --region us-east-1 --query 'StackSummaries[?contains(StackName, `SecurityChatbot`)]'

# Verify AgentCore resources
agentcore status

# Test MCP server
cd src/mcp-server && python3 -m pytest tests/

# Test end-to-end flow
agentcore invoke '{"prompt": "What is my security status?"}'
```

### Health Checks
```bash
# Check CloudWatch dashboards
aws cloudwatch list-dashboards --region us-east-1

# Check alarms status
aws cloudwatch describe-alarms --region us-east-1 --alarm-names SecurityChatbot*

# Check costs
aws ce get-cost-and-usage --time-period Start=2025-01-01,End=2025-01-31 --granularity MONTHLY --metrics BlendedCost
```

## 🚨 Troubleshooting

### Common Issues
```bash
# CDK bootstrap issues
cdk bootstrap --force aws://$AWS_ACCOUNT_ID/us-east-1

# Permission issues
aws iam get-user  # Verify user permissions
aws sts assume-role --role-arn arn:aws:iam::$AWS_ACCOUNT_ID:role/CDKExecRole

# AgentCore service limits
aws service-quotas get-service-quota --service-code bedrock --quota-code L-12345

# Stack dependency issues
cdk deploy SecurityChatbot-dev-Security --exclusively
cdk deploy SecurityChatbot-dev-AgentCore --exclusively
cdk deploy SecurityChatbot-dev-Monitoring --exclusively
```

### Rollback Procedures
```bash
# Rollback to previous version
cdk deploy --rollback

# Emergency stack removal
aws cloudformation delete-stack --stack-name SecurityChatbot-dev-AgentCore --region us-east-1

# Force resource cleanup
aws cloudformation continue-update-rollback --stack-name SecurityChatbot-dev-AgentCore --region us-east-1
```

## 📈 Cost Optimization

### Environment Sizing
- **Development**: Minimal resources, auto-destroy after 7 days
- **Staging**: Production-like but smaller scale
- **Production**: Full scale with high availability

### Cost Monitoring
```bash
# Set up cost alerts
aws budgets create-budget --account-id $AWS_ACCOUNT_ID --budget file://budget.json

# Monitor daily costs
aws ce get-cost-and-usage --time-period Start=$(date -d '7 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) --granularity DAILY --metrics BlendedCost
```

## 🎯 Success Criteria

✅ **Deployment Success**:
- All 3 stacks deploy without errors
- AgentCore resources created and accessible
- MCP server responds to test queries
- Monitoring dashboards populated

✅ **Repeatability Success**:
- Same deployment works in different accounts
- Clean removal leaves no orphaned resources
- Re-deployment after removal works identically
- All configurations parameterized properly

**Remember: Infrastructure as Code means predictable, repeatable, and reliable deployments every time!**
