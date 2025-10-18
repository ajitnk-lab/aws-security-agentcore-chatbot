#!/usr/bin/env python3
"""
Test Gateway connection to AgentCore Runtime right now
"""
import json
import requests

def test_gateway():
    # Load gateway config
    with open('gateway_config.json', 'r') as f:
        config = json.load(f)
    
    print(f"Testing Gateway: {config['gateway_url']}")
    
    # Get fresh token
    print("Getting fresh token...")
    token_response = requests.post(config['token_endpoint'], data={
        'grant_type': 'client_credentials',
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'scope': config['scope']
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    
    if token_response.status_code != 200:
        print(f"❌ Token failed: {token_response.text}")
        return False
    
    token = token_response.json()['access_token']
    print("✅ Token obtained")
    
    # Test tools/list
    print("Testing tools/list...")
    list_response = requests.post(config['gateway_url'], 
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'tools/list'
        }
    )
    
    if list_response.status_code != 200:
        print(f"❌ Tools list failed: {list_response.text}")
        return False
    
    result = list_response.json()
    if 'result' not in result or 'tools' not in result['result']:
        print(f"❌ Invalid response: {result}")
        return False
    
    tools = result['result']['tools']
    print(f"✅ Found {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool['name']}")
    
    # Test calling a security tool
    print("\nTesting CheckSecurityServices...")
    call_response = requests.post(config['gateway_url'], 
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'tools/call',
            'params': {
                'name': 'SecurityMCPTools___CheckSecurityServices',
                'arguments': {'region': 'us-east-1'}
            }
        }
    )
    
    print(f"Status: {call_response.status_code}")
    call_result = call_response.json()
    
    if 'error' in call_result:
        print(f"❌ Tool call failed: {call_result['error']}")
        return False
    
    if 'result' in call_result:
        print("✅ Tool call successful!")
        print(f"Result: {json.dumps(call_result['result'], indent=2)}")
        return True
    
    print(f"❌ Unexpected response: {call_result}")
    return False

if __name__ == "__main__":
    success = test_gateway()
    print(f"\n{'✅ Gateway is working!' if success else '❌ Gateway has issues'}")
