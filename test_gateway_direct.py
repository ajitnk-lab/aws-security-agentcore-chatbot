#!/usr/bin/env python3

import requests
import json
import boto3

def get_cognito_token():
    """Get OAuth token from Cognito"""
    cognito = boto3.client('cognito-idp', region_name='us-east-1')
    
    try:
        # Use client credentials flow for machine-to-machine auth
        response = cognito.initiate_auth(
            ClientId='31tulnklmj2kcslkmgcbme7n9v',
            AuthFlow='CLIENT_CREDENTIALS'
        )
        return response['AuthenticationResult']['AccessToken']
    except Exception as e:
        print(f"Failed to get token: {e}")
        return None

def test_gateway():
    """Test Gateway directly"""
    gateway_url = "https://security-runtime-gateway-dtga85g9fh.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
    
    # Try without auth first
    print("Testing Gateway without authentication...")
    try:
        response = requests.post(
            gateway_url,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            },
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gateway()
