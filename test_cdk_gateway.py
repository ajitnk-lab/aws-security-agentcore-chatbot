#!/usr/bin/env python3

import requests
import json
import boto3

def test_gateway():
    # Gateway URL from CDK outputs
    gateway_url = "https://security-chatbot-gateway-41f3cc60-fmqz5lmy6j.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
    
    # Get Cognito token
    cognito = boto3.client('cognito-idp', region_name='us-east-1')
    
    try:
        # Test without authentication first to see what happens
        print("Testing Gateway without authentication...")
        response = requests.post(
            gateway_url,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error testing gateway: {e}")

if __name__ == "__main__":
    test_gateway()
