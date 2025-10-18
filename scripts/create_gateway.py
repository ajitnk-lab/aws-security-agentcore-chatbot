#!/usr/bin/env python3
"""
Create AgentCore Gateway for Security Chatbot MCP Server
"""

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json
import time

def create_security_gateway():
    """Create AgentCore Gateway with MCP server target"""
    
    region = "us-east-1"
    
    print("🚀 Setting up AgentCore Gateway for Security Chatbot...")
    print(f"Region: {region}\n")
    
    # Initialize client
    client = GatewayClient(region_name=region)
    
    # Step 1: Create OAuth authorizer
    print("Step 1: Creating OAuth authorization server...")
    cognito_response = client.create_oauth_authorizer_with_cognito("SecurityChatbotGateway")
    print("✓ Authorization server created\n")
    
    # Step 2: Create Gateway
    print("Step 2: Creating Gateway...")
    gateway = client.create_mcp_gateway(
        name=f"SecurityChatbotGateway-{int(time.time())}",  # Unique name
        role_arn=None,  # Will be auto-created
        authorizer_config=cognito_response["authorizer_config"],
        enable_semantic_search=True,
    )
    print(f"✓ Gateway created: {gateway['gatewayUrl']}\n")
    
    # Fix IAM permissions
    client.fix_iam_permissions(gateway)
    print("⏳ Waiting 30s for IAM propagation...")
    time.sleep(30)
    print("✓ IAM permissions configured\n")
    
    # Step 3: Add our deployed MCP server as a target
    print("Step 3: Adding MCP server runtime as target...")
    
    # Get the runtime ARN from our deployment
    runtime_arn = "arn:aws:bedrock-agentcore:us-east-1:039920874011:runtime/agentcore_mcp_server-CmiD0a32zF"
    
    # Create target payload for our MCP server runtime
    target_payload = {
        "lambdaArn": runtime_arn,  # AgentCore Runtime ARN
        "toolSchema": {
            "inlinePayload": [
                {
                    "name": "CheckSecurityServices",
                    "description": "Check if AWS security services are enabled",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "AWS region to check (optional)"
                            }
                        }
                    }
                },
                {
                    "name": "GetSecurityFindings",
                    "description": "Get security findings from multiple AWS services",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "AWS region to check (optional)"
                            },
                            "severity": {
                                "type": "string",
                                "description": "Filter by severity (HIGH, MEDIUM, LOW)"
                            }
                        }
                    }
                },
                {
                    "name": "CheckStorageEncryption",
                    "description": "Check storage encryption compliance",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "AWS region to check (optional)"
                            }
                        }
                    }
                },
                {
                    "name": "CheckNetworkSecurity",
                    "description": "Check network security configurations",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "AWS region to check (optional)"
                            }
                        }
                    }
                },
                {
                    "name": "ListServicesInRegion",
                    "description": "List AWS services in use in a region",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "AWS region to check"
                            }
                        },
                        "required": ["region"]
                    }
                },
                {
                    "name": "GetStoredSecurityContext",
                    "description": "Get stored security context from previous assessments",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "context_id": {
                                "type": "string",
                                "description": "Context identifier (optional)"
                            }
                        }
                    }
                }
            ]
        }
    }
    
    # Create the target
    mcp_target = client.create_mcp_gateway_target(
        gateway=gateway,
        name="SecurityMCPServer",
        target_type="lambda",
        target_payload=target_payload,
        credentials=None  # Use Gateway IAM role
    )
    print("✓ MCP server target added\n")
    
    # Step 4: Save configuration
    config = {
        "gateway_url": gateway["gatewayUrl"],
        "gateway_id": gateway["gatewayId"],
        "region": region,
        "client_info": cognito_response["client_info"],
        "runtime_arn": runtime_arn,
        "target_id": mcp_target["targetId"]
    }
    
    with open('gateway_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("=" * 60)
    print("✅ Gateway setup complete!")
    print(f"Gateway URL: {gateway['gatewayUrl']}")
    print(f"Gateway ID: {gateway['gatewayId']}")
    print(f"Target ID: {mcp_target['targetId']}")
    print("\nConfiguration saved to: gateway_config.json")
    print("=" * 60)
    
    return config

if __name__ == "__main__":
    config = create_security_gateway()
    print(f"\n🎯 Next steps:")
    print(f"1. Test gateway connectivity")
    print(f"2. Create Bedrock Agent integration")
    print(f"3. Build chat interface")
