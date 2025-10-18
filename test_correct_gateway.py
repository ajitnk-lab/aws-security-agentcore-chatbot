#!/usr/bin/env python3
"""
Test the CORRECT Gateway from CDK outputs
"""
import json
import requests

def test_correct_gateway():
    # Use the Gateway from CDK outputs, not the old one
    gateway_url = "https://security-chatbot-gateway-development.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
    
    print(f"Testing CORRECT Gateway: {gateway_url}")
    
    # This Gateway might have different OAuth config
    # Let me check if there's a config file for it
    try:
        with open('cdk-outputs.json', 'r') as f:
            outputs = json.load(f)
        
        user_pool_id = outputs['SecurityChatbot-development-Security']['ExportsOutputRefSecurityChatbotUserPoolE20E651A5DC49B17']
        print(f"User Pool ID: {user_pool_id}")
        
        # Try without authentication first to see what error we get
        response = requests.post(gateway_url, 
            headers={'Content-Type': 'application/json'},
            json={'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_correct_gateway()
