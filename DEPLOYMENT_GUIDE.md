# AWS Security AgentCore Chatbot - Deployment Guide

## 🎯 Complete Deployment Process

### Prerequisites
- AWS CLI configured with appropriate permissions
- Node.js 18+ and Python 3.10+
- AgentCore CLI installed: `pip install bedrock-agentcore-starter-toolkit`

### Step 1: CDK Infrastructure Deployment
```bash
# Clone repository
git clone https://github.com/ajitnk-lab/aws-security-agentcore-chatbot.git
cd aws-security-agentcore-chatbot

# Install dependencies
npm install
pip install -r requirements.txt

# Deploy CDK stacks (IAM roles, Cognito, monitoring)
cdk deploy --all
```

### Step 2: AgentCore Resources Deployment
```bash
# Deploy AgentCore Memory, Runtime, and Gateway
./scripts/deploy_agentcore.sh development
```

This script will:
1. **Create AgentCore Memory** with semantic strategies
2. **Deploy AgentCore Runtime** with MCP server hosting 7 security tools
3. **Create AgentCore Gateway** with OAuth2 authentication
4. **Test the complete integration** to verify connectivity

### Step 3: Verify Deployment
```bash
# Test Gateway-Runtime connection
python3 scripts/test_gateway_runtime_connection.py

# Expected output: 7 security tools accessible via MCP protocol
```

## 🏗️ Architecture Deployed

```
Chat UI ↔ Bedrock Agent ↔ AgentCore Gateway ↔ AgentCore Runtime ↔ MCP Server ↔ AWS Security Services
```

### Resources Created:
- **AgentCore Memory**: Semantic memory with user preferences and security context
- **AgentCore Runtime**: Serverless runtime hosting MCP server with 7 security tools
- **AgentCore Gateway**: OAuth2-secured gateway exposing MCP protocol
- **IAM Roles**: Least-privilege roles for all components
- **Cognito User Pool**: Authentication for Gateway access
- **CloudWatch**: Monitoring and logging for all components

## 🔧 Configuration Files Generated

After deployment, these files contain your environment-specific configuration:

- `memory_config.json`: Memory resource ID and configuration
- `gateway_config.json`: Gateway URL, OAuth credentials, and access tokens
- `.bedrock_agentcore.yaml`: Runtime configuration (auto-generated)

## 🧪 Testing Your Deployment

### Test 1: Memory Operations
```bash
python3 scripts/test_memory.py
```

### Test 2: Gateway Authentication
```bash
python3 scripts/test_gateway_runtime_connection.py
```

### Test 3: Security Tools
The Gateway should expose these 7 tools:
1. `CheckSecurityServices` - AWS security services status
2. `CheckStorageEncryption` - Storage encryption validation
3. `CheckNetworkSecurity` - Network security analysis
4. `GetSecurityFindings` - Security findings retrieval
5. `ListServicesInRegion` - Service discovery
6. `GetStoredSecurityContext` - Security context storage
7. `x_amz_bedrock_agentcore_search` - Tool discovery

## 🌍 Multi-Account/Environment Deployment

### Deploy to Different Environment
```bash
# Deploy to staging
cdk deploy --all -c environment=staging
./scripts/deploy_agentcore.sh staging

# Deploy to production  
cdk deploy --all -c environment=production
./scripts/deploy_agentcore.sh production
```

### Cross-Account Deployment
1. Configure AWS CLI for target account
2. Update `cdk.json` with target account ID
3. Run deployment commands as above

## 🔒 Security Considerations

- All resources use least-privilege IAM roles
- Gateway uses OAuth2 with Cognito for authentication
- All data encrypted at rest and in transit
- Audit logging enabled for all operations
- Network security groups restrict access

## 💰 Cost Optimization

- AgentCore Runtime uses serverless pricing (pay-per-use)
- Memory retention configurable (7-30 days)
- CloudWatch logs with retention policies
- Auto-scaling based on demand

## 🚨 Troubleshooting

### Common Issues:

1. **Gateway target fails with OAuth error**
   ```bash
   python3 scripts/fix_oauth_configuration.py
   ```

2. **Runtime deployment fails**
   - Check AWS credentials and permissions
   - Verify AgentCore CLI installation
   - Check region configuration (must be us-east-1)

3. **Memory operations fail**
   - Verify Memory resource was created successfully
   - Check IAM permissions for Memory access

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ajitnk-lab/aws-security-agentcore-chatbot/issues)
- **Documentation**: Project README and architecture docs
- **Logs**: Check CloudWatch logs for detailed error information
