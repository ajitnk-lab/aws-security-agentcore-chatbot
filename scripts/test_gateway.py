#!/usr/bin/env python3
"""
Test AgentCore Gateway connectivity and tool calling

This script tests the Gateway MCP endpoints and validates that external
agents can successfully authenticate and call security tools.
"""

import json
import asyncio
import httpx
from datetime import datetime, timedelta

class GatewayTokenManager:
    """Manages OAuth tokens with automatic refresh"""
    
    def __init__(self, client_id, client_secret, token_endpoint, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self.scope = scope
        self._token = None
        self._expires_at = None
    
    async def get_token(self):
        """Get valid token, refreshing if needed"""
        if self._token and self._expires_at > datetime.now():
            return self._token
        
        # Fetch new token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_endpoint,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'scope': self.scope
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code != 200:
                raise Exception(f"Token request failed: {response.status_code} - {response.text}")
            
            data = response.json()
            self._token = data['access_token']
            # Buffer expiry by 5 minutes
            expires_in = data.get('expires_in', 3600) - 300
            self._expires_at = datetime.now() + timedelta(seconds=expires_in)
            return self._token

async def call_gateway_tool(gateway_url, token_manager, tool_name, arguments):
    """Call a tool through the Gateway using MCP protocol"""
    token = await token_manager.get_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            gateway_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Tool call failed: {response.status_code} - {response.text}")
        
        result = response.json()
        if 'error' in result:
            raise Exception(f"Tool error: {result['error']}")
        
        return result.get('result')

async def list_gateway_tools(gateway_url, token_manager):
    """List available tools from the Gateway"""
    token = await token_manager.get_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            gateway_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Tools list failed: {response.status_code} - {response.text}")
        
        result = response.json()
        if 'error' in result:
            raise Exception(f"Tools list error: {result['error']}")
        
        return result.get('result', {}).get('tools', [])

async def main():
    print("🧪 Testing AgentCore Gateway...")
    
    # Load gateway configuration
    try:
        with open("gateway_config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Gateway config not found. Run setup_gateway.py first.")
        return False
    
    # Initialize token manager
    token_manager = GatewayTokenManager(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        token_endpoint=config['token_endpoint'],
        scope=config['scope']
    )
    
    gateway_url = config['gateway_url']
    
    try:
        # Test 1: Authentication
        print("🔐 Testing authentication...")
        token = await token_manager.get_token()
        print(f"✅ Successfully obtained access token: {token[:20]}...")
        
        # Test 2: List available tools
        print("\n📋 Listing available tools...")
        tools = await list_gateway_tools(gateway_url, token_manager)
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
        
        # Test 3: Call security service check
        print("\n🔍 Testing CheckSecurityServices tool...")
        result = await call_gateway_tool(
            gateway_url, 
            token_manager, 
            "SecurityMCPTools___CheckSecurityServices", 
            {"region": "us-east-1"}
        )
        print("✅ CheckSecurityServices result:")
        print(json.dumps(result, indent=2))
        
        # Test 4: Call list services
        print("\n📊 Testing ListServicesInRegion tool...")
        result = await call_gateway_tool(
            gateway_url, 
            token_manager, 
            "SecurityMCPTools___ListServicesInRegion", 
            {"region": "us-east-1"}
        )
        print("✅ ListServicesInRegion result:")
        print(json.dumps(result, indent=2))
        
        print("\n🎉 All Gateway tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Gateway test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)
