#!/usr/bin/env python3
"""
Setup AgentCore Gateway for AWS Security Chatbot

This script creates a Gateway that exposes our security tools as MCP endpoints
for external agents to consume.
"""

import json
import os
import sys
import time
import uuid
from bedrock_agentcore_starter_toolkit.operations.gateway import GatewayClient

def main():
    print("🚀 Setting up AgentCore Gateway for Security Tools...")
    
    # Initialize Gateway client
    client = GatewayClient(region_name='us-east-1')
    
    # Create unique gateway name
    gateway_name = f"security-chatbot-gateway-{uuid.uuid4().hex[:8]}"
    
    # Create OAuth authorizer with Cognito
    print("📝 Creating OAuth authorization server...")
    cognito_response = client.create_oauth_authorizer_with_cognito(gateway_name)
    print("✅ Authorization server created")
    
    # Create Gateway
    print("🔧 Creating AgentCore Gateway...")
    gateway = client.create_mcp_gateway(
        name=gateway_name,
        role_arn="arn:aws:iam::039920874011:role/AgentCoreGatewayExecutionRole",
        authorizer_config=cognito_response['authorizer_config'],
        enable_semantic_search=True,
    )
    print(f"✅ Gateway created: {gateway['gatewayUrl']}")
    
    # Fix IAM permissions
    print("🔧 Fixing IAM permissions...")
    client.fix_iam_permissions(gateway)
    print("⏳ Waiting 30s for IAM propagation...")
    time.sleep(30)
    print("✅ IAM permissions configured")
    
    # Define our security tools schema for Lambda target
    security_tools_schema = {
        "inlinePayload": [
            {
                "name": "CheckSecurityServices",
                "description": "Check status of AWS security services (GuardDuty, Security Hub, Inspector)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string", "description": "AWS region to check"}
                    },
                    "required": ["region"]
                }
            },
            {
                "name": "GetSecurityFindings",
                "description": "Retrieve security findings from multiple AWS services",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string", "description": "AWS region to check"},
                        "severity": {"type": "string", "description": "Filter by severity (HIGH, MEDIUM, LOW)"}
                    },
                    "required": ["region"]
                }
            },
            {
                "name": "CheckStorageEncryption",
                "description": "Check encryption status of storage services (S3, EBS, RDS)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string", "description": "AWS region to check"}
                    },
                    "required": ["region"]
                }
            },
            {
                "name": "CheckNetworkSecurity",
                "description": "Analyze network security configuration (Security Groups, NACLs, Load Balancers)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string", "description": "AWS region to check"}
                    },
                    "required": ["region"]
                }
            },
            {
                "name": "ListServicesInRegion",
                "description": "List AWS services in use in a specific region",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string", "description": "AWS region to check"}
                    },
                    "required": ["region"]
                }
            },
            {
                "name": "GetStoredSecurityContext",
                "description": "Retrieve stored security context and recommendations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "context_type": {"type": "string", "description": "Type of context to retrieve"}
                    }
                }
            }
        ]
    }
    
    # Add Lambda target for our MCP server
    print("🔧 Adding security tools Lambda target...")
    lambda_target = client.create_mcp_gateway_target(
        gateway=gateway,
        name="SecurityMCPTools",
        target_type="lambda",
        target_payload={
            "lambdaArn": "arn:aws:lambda:us-east-1:039920874011:function:security-gateway-mcp-handler",
            "toolSchema": security_tools_schema
        }
    )
    print("✅ Security tools target added")
    
    # Get access token
    print("🔑 Getting access token...")
    access_token = client.get_access_token_for_cognito(cognito_response["client_info"])
    print("✅ Access token obtained")
    
    # Save configuration for external agents
    config = {
        "gateway_url": gateway["gatewayUrl"],
        "gateway_id": gateway["gatewayId"],
        "client_id": cognito_response['client_info']['client_id'],
        "client_secret": cognito_response['client_info']['client_secret'],
        "token_endpoint": cognito_response['client_info']['token_endpoint'],
        "scope": cognito_response['client_info']['scope'],
        "access_token": access_token
    }
    
    # Save to multiple locations for different use cases
    config_file = "gateway_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    # Also save to infrastructure directory for CDK
    os.makedirs("infrastructure", exist_ok=True)
    infra_config_file = "infrastructure/gateway_config.json"
    with open(infra_config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "="*60)
    print("✅ Gateway setup complete!")
    print(f"Gateway URL: {gateway['gatewayUrl']}")
    print(f"Gateway ID: {gateway['gatewayId']}")
    print(f"Configuration saved to: {config_file}")
    print(f"Infrastructure config: {infra_config_file}")
    print("\n🔑 OAuth Credentials:")
    print(f"Client ID: {config['client_id']}")
    print(f"Token Endpoint: {config['token_endpoint']}")
    print("="*60)
    
    return config

if __name__ == "__main__":
    try:
        config = main()
        print("\n🎉 Gateway setup successful!")
        print("External agents can now connect to the security tools via MCP protocol.")
    except Exception as e:
        print(f"❌ Error setting up gateway: {e}")
        sys.exit(1)
