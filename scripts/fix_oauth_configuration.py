#!/usr/bin/env python3
"""
Fix OAuth configuration between Gateway and Runtime.

The Gateway target was created successfully but failed with "Please check the OAuth setup".
This script addresses the authentication configuration between Gateway and Runtime.
"""

import json
import logging
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

def main():
    print("🔧 Fixing OAuth configuration between Gateway and Runtime...")
    
    # Initialize Gateway client
    client = GatewayClient(region_name="us-east-1")
    client.logger.setLevel(logging.INFO)
    
    # Load existing gateway configuration
    try:
        with open("gateway_config.json", "r") as f:
            config = json.load(f)
        gateway_id = config["gateway_id"]
        print(f"Gateway ID: {gateway_id}")
    except FileNotFoundError:
        print("❌ gateway_config.json not found.")
        return
    
    # The issue is that the Runtime needs to be configured to accept requests from the Gateway
    # Based on the AgentCore architecture, there are a few possible solutions:
    
    print("\n📋 OAuth Configuration Analysis:")
    print("1. Gateway target created successfully with endpoint:")
    print("   https://agentcore_mcp_server-CmiD0a32zF.runtime.bedrock-agentcore.us-east-1.amazonaws.com")
    print("2. Target failed with 'Please check the OAuth setup'")
    print("3. This suggests the Runtime is not configured to accept Gateway requests")
    
    print("\n🔍 Possible Solutions:")
    print("1. Runtime may need to be configured with Gateway credentials")
    print("2. Gateway IAM role may need additional permissions")
    print("3. Runtime may need to be redeployed with Gateway integration")
    
    # Check if we can fix IAM permissions
    try:
        gateway_obj = {"gatewayId": gateway_id}
        print("\n🔧 Attempting to fix IAM permissions...")
        client.fix_iam_permissions(gateway_obj)
        print("✅ IAM permissions updated")
        
        # Wait for propagation
        import time
        print("⏳ Waiting 30s for IAM propagation...")
        time.sleep(30)
        
        print("✅ OAuth configuration fix completed")
        print("\n📝 Next Steps:")
        print("1. Test the Gateway connection")
        print("2. If still failing, Runtime may need Gateway integration configuration")
        print("3. Check Runtime logs for authentication errors")
        
    except Exception as e:
        print(f"❌ Error fixing IAM permissions: {e}")
        
        print("\n🔧 Manual Fix Required:")
        print("The Runtime was deployed independently and may not be configured")
        print("to accept requests from the Gateway. You may need to:")
        print("1. Redeploy the Runtime with Gateway integration enabled")
        print("2. Configure the Runtime with Gateway OAuth credentials")
        print("3. Update Runtime IAM role to allow Gateway access")

if __name__ == "__main__":
    main()
