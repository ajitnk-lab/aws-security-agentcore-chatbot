#!/usr/bin/env python3
"""
Fix Gateway-Runtime connection using the correct target configuration.

Based on the error "mcpServer target type requires 'endpoint' parameter, not 'runtimeArn'",
this script creates the correct Gateway target configuration to connect to the existing Runtime.
"""

import json
import logging
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

def main():
    runtime_arn = "arn:aws:bedrock-agentcore:us-east-1:039920874011:runtime/agentcore_mcp_server-CmiD0a32zF"
    
    print("🔧 Fixing Gateway-Runtime connection...")
    print(f"Runtime ARN: {runtime_arn}")
    
    # Initialize Gateway client
    client = GatewayClient(region_name="us-east-1")
    client.logger.setLevel(logging.INFO)
    
    # Load existing gateway configuration
    try:
        with open("gateway_config.json", "r") as f:
            config = json.load(f)
        gateway_id = config["gateway_id"]
        print(f"Found existing Gateway: {gateway_id}")
    except FileNotFoundError:
        print("❌ gateway_config.json not found. Please run setup_gateway.py first.")
        return
    
    # Get gateway object
    gateway = {"gatewayId": gateway_id}
    
    print("Creating Runtime target...")
    
    try:
        # Based on the documentation and error message, we need to use the correct approach
        # The error suggests mcpServer target type needs "endpoint", but we have a Runtime ARN
        # Let's try using the Runtime ARN as a different target type
        
        # Option 1: Try using runtime target type (if it exists)
        try:
            runtime_target = client.create_mcp_gateway_target(
                gateway=gateway,
                name="SecurityMCPServer",
                target_type="runtime",  # Try runtime instead of mcpServer
                target_payload={
                    "runtimeArn": runtime_arn
                }
            )
            print("✅ Runtime target created successfully!")
            print(f"Target: {runtime_target}")
            return
            
        except Exception as e1:
            print(f"Runtime target type failed: {e1}")
            
            # Option 2: Try using agentcore target type
            try:
                agentcore_target = client.create_mcp_gateway_target(
                    gateway=gateway,
                    name="SecurityMCPServer", 
                    target_type="agentcore",
                    target_payload={
                        "runtimeArn": runtime_arn
                    }
                )
                print("✅ AgentCore target created successfully!")
                print(f"Target: {agentcore_target}")
                return
                
            except Exception as e2:
                print(f"AgentCore target type failed: {e2}")
                
                # Option 3: If we need an endpoint URL, construct it from the Runtime ARN
                # Based on AWS patterns, the Runtime should be accessible via HTTPS
                runtime_id = runtime_arn.split('/')[-1]  # agentcore_mcp_server-CmiD0a32zF
                region = runtime_arn.split(':')[3]  # us-east-1
                
                # Try different endpoint URL patterns
                possible_endpoints = [
                    f"https://{runtime_id}.runtime.bedrock-agentcore.{region}.amazonaws.com",
                    f"https://runtime.bedrock-agentcore.{region}.amazonaws.com/{runtime_id}",
                    f"https://bedrock-agentcore.{region}.amazonaws.com/runtime/{runtime_id}",
                ]
                
                for endpoint_url in possible_endpoints:
                    try:
                        print(f"Trying endpoint: {endpoint_url}")
                        mcp_target = client.create_mcp_gateway_target(
                            gateway=gateway,
                            name="SecurityMCPServer",
                            target_type="mcpServer",
                            target_payload={
                                "endpoint": endpoint_url
                            }
                        )
                        print("✅ MCP Server target created successfully!")
                        print(f"Target: {mcp_target}")
                        print(f"Endpoint URL: {endpoint_url}")
                        return
                        
                    except Exception as e3:
                        print(f"Endpoint {endpoint_url} failed: {e3}")
                        continue
                
                print("❌ All target configuration attempts failed.")
                print("\nNext steps:")
                print("1. Check AgentCore documentation for correct Runtime endpoint URL format")
                print("2. Verify Runtime is accessible and running")
                print("3. Check if there's a specific target type for AgentCore Runtimes")
                
    except Exception as e:
        print(f"❌ Error creating Gateway target: {e}")
        print("\nThis confirms we need the correct target configuration approach.")

if __name__ == "__main__":
    main()
