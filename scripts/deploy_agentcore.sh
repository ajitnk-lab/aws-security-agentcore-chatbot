#!/bin/bash
set -e

# Deploy AgentCore resources after CDK deployment
# This script should be run after: cdk deploy --all

echo "🚀 Deploying AgentCore Resources..."

# Get environment from parameter or default
ENVIRONMENT=${1:-development}
REGION="us-east-1"

echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

# Step 1: Create AgentCore Memory
echo "📝 Creating AgentCore Memory..."
python3 scripts/create_memory.py

# Step 2: Deploy AgentCore Runtime with MCP Server
echo "🏃 Deploying AgentCore Runtime..."
agentcore configure -e agent.py
agentcore launch

# Step 3: Create AgentCore Gateway
echo "🌉 Creating AgentCore Gateway..."
python3 scripts/setup_gateway.py

# Step 4: Test the complete integration
echo "🧪 Testing Gateway-Runtime connection..."
python3 scripts/test_gateway_runtime_connection.py

echo "✅ AgentCore deployment completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Create Bedrock Agent and connect to Gateway"
echo "2. Test end-to-end security analysis workflow"
echo "3. Deploy chat interface"
