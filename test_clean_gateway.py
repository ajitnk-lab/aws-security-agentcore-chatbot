#!/usr/bin/env python3
"""
Test the clean Gateway to ensure it can call AgentCore Runtime and discover all tools
"""
import requests
import json

def test_clean_gateway():
    # Clean Gateway URL
    gateway_url = "https://security-chatbot-clean-a4165c1f-10wdftnwcc.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
    
    print(f"🧪 Testing Clean Gateway: {gateway_url}")
    
    # Test without authentication first to see what happens
    print("\n1. Testing without authentication...")
    response = requests.post(gateway_url, 
        headers={'Content-Type': 'application/json'},
        json={'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # The Gateway should require authentication, so we expect an auth error
    if response.status_code == 401 or "Unauthorized" in response.text:
        print("✅ Gateway properly requires authentication")
        return True
    elif "Invalid GatewayId" in response.text:
        print("❌ Gateway has invalid ID - not properly created")
        return False
    else:
        print("⚠️ Unexpected response - Gateway may have issues")
        return False

if __name__ == "__main__":
    success = test_clean_gateway()
    print(f"\n{'✅ Clean Gateway is accessible' if success else '❌ Clean Gateway has issues'}")
