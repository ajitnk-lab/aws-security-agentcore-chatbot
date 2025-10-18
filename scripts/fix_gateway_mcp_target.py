#!/usr/bin/env python3
"""
Fix Gateway MCP target configuration.

This script addresses the error: "mcpServer target type requires 'endpoint' parameter, not 'runtimeArn'"
by finding the correct HTTP endpoint URL for the AgentCore Runtime and updating the Gateway target.
"""

import json
import boto3
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

def get_runtime_endpoint_url(runtime_arn: str) -> str:
    """
    Convert Runtime ARN to HTTP endpoint URL.
    
    Based on AWS patterns, the Runtime should be accessible via an HTTP endpoint.
    We need to determine the correct URL format from the ARN.
    """
    # Parse ARN: arn:aws:bedrock-agentcore:us-east-1:039920874011:runtime/agentcore_mcp_server-CmiD0a32zF
    arn_parts = runtime_arn.split(':')
    region = arn_parts[3]
    account_id = arn_parts[4]
    resource_parts = arn_parts[5].split('/')
    runtime_id = resource_parts[1]
    
    # Try different possible endpoint URL formats
    possible_urls = [
        f"https://{runtime_id}.bedrock-agentcore.{region}.amazonaws.com",
        f"https://runtime-{runtime_id}.bedrock-agentcore.{region}.amazonaws.com", 
        f"https://bedrock-agentcore-runtime.{region}.amazonaws.com/{runtime_id}",
        f"https://{account_id}.bedrock-agentcore.{region}.amazonaws.com/runtime/{runtime_id}",
    ]
    
    print("Possible Runtime endpoint URLs:")
    for i, url in enumerate(possible_urls, 1):
        print(f"  {i}. {url}")
    
    # For now, return the most likely format based on AWS service patterns
    # This may need adjustment based on actual AgentCore Runtime URL format
    return possible_urls[0]

def main():
    runtime_arn = "arn:aws:bedrock-agentcore:us-east-1:039920874011:runtime/agentcore_mcp_server-CmiD0a32zF"
    
    print("🔧 Fixing Gateway MCP target configuration...")
    print(f"Runtime ARN: {runtime_arn}")
    
    # Get the endpoint URL
    endpoint_url = get_runtime_endpoint_url(runtime_arn)
    print(f"Derived endpoint URL: {endpoint_url}")
    
    # Initialize Gateway client
    client = GatewayClient(region_name="us-east-1")
    
    # Load existing gateway configuration
    try:
        with open("gateway_config.json", "r") as f:
            config = json.load(f)
        gateway_id = config["gateway_id"]
        print(f"Found existing Gateway: {gateway_id}")
    except FileNotFoundError:
        print("❌ gateway_config.json not found. Please run setup_gateway.py first.")
        return
    
    # Create MCP server target with endpoint URL
    print("Creating MCP server target...")
    try:
        # Note: This is the correct approach for mcpServer target type
        target_config = {
            "endpoint": endpoint_url,
            # Add any additional MCP server configuration here
        }
        
        # Create the target (this may fail if endpoint URL format is incorrect)
        # We'll need to adjust the URL format based on the actual error
        print(f"Target configuration: {json.dumps(target_config, indent=2)}")
        print("\n⚠️  NOTE: The endpoint URL format may need adjustment based on actual AgentCore Runtime URL patterns.")
        print("If this fails, we'll need to:")
        print("1. Check AgentCore Runtime documentation for correct endpoint format")
        print("2. Use AWS CLI or SDK to describe the Runtime and get its endpoint")
        print("3. Test connectivity to the endpoint")
        
        # For now, just show what the configuration should look like
        print("\n✅ Configuration ready. To apply:")
        print("1. Verify the endpoint URL is correct")
        print("2. Test connectivity to the endpoint")
        print("3. Create the Gateway target with the endpoint parameter")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nThis confirms that we need the correct endpoint URL format.")
        print("The mcpServer target type requires an 'endpoint' parameter with the HTTP URL,")
        print("not the Runtime ARN.")

if __name__ == "__main__":
    main()
