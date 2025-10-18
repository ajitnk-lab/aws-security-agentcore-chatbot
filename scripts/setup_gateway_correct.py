#!/usr/bin/env python3
"""
Setup AgentCore Gateway - CORRECT VERSION
Connects Gateway to AgentCore Runtime MCP server (not Lambda)
Following original architecture exactly
"""

import json
import os
import sys
import time
import uuid
from bedrock_agentcore_starter_toolkit.operations.gateway import GatewayClient

def main():
    print("🚀 Setting up AgentCore Gateway (CORRECT - connects to Runtime)")
    
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
    
    # Add AgentCore Runtime target (NOT Lambda)
    print("🔧 Adding AgentCore Runtime MCP server target...")
    runtime_target = client.create_mcp_gateway_target(
        gateway=gateway,
        name="SecurityMCPRuntime",
        target_type="mcpServer",  # Correct type for MCP server
        target_payload={
            "runtimeArn": "arn:aws:bedrock-agentcore:us-east-1:039920874011:runtime/agentcore_mcp_server-CmiD0a32zF"
        }
    )
    print("✅ AgentCore Runtime target added")
    
    # Get access token
    print("🔑 Getting access token...")
    access_token = client.get_access_token_for_cognito(cognito_response["client_info"])
    print("✅ Access token obtained")
    
    # Save configuration
    config = {
        "gateway_url": gateway["gatewayUrl"],
        "gateway_id": gateway["gatewayId"],
        "client_id": cognito_response['client_info']['client_id'],
        "client_secret": cognito_response['client_info']['client_secret'],
        "token_endpoint": cognito_response['client_info']['token_endpoint'],
        "scope": cognito_response['client_info']['scope'],
        "access_token": access_token,
        "runtime_arn": "arn:aws:bedrock-agentcore:us-east-1:039920874011:runtime/agentcore_mcp_server-CmiD0a32zF"
    }
    
    with open("gateway_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "="*60)
    print("✅ Gateway setup complete!")
    print(f"Gateway URL: {gateway['gatewayUrl']}")
    print(f"Connected to Runtime: agentcore_mcp_server-CmiD0a32zF")
    print("="*60)
    
    return config

if __name__ == "__main__":
    try:
        config = main()
        print("\n🎉 Gateway correctly connected to AgentCore Runtime!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
