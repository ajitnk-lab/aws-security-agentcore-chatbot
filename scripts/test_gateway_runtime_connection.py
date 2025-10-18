#!/usr/bin/env python3
"""
Test Gateway-Runtime connection to verify the OAuth fix worked.
"""

import json
import asyncio
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def test_gateway_connection():
    """Test the Gateway MCP connection"""
    
    # Load gateway configuration
    try:
        with open("gateway_config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ gateway_config.json not found.")
        return False
    
    gateway_url = config["gateway_url"]
    access_token = config["access_token"]
    
    print(f"🔗 Testing Gateway connection...")
    print(f"Gateway URL: {gateway_url}")
    
    try:
        # Test basic HTTP connectivity
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            # Test basic connectivity
            response = await client.get(gateway_url, headers=headers, timeout=10.0)
            print(f"HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Gateway HTTP connection successful")
            else:
                print(f"⚠️  Gateway returned status {response.status_code}")
                print(f"Response: {response.text[:200]}...")
        
        # Test MCP protocol
        print("\n🔌 Testing MCP protocol connection...")
        
        async with streamablehttp_client(gateway_url, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # List available tools
                tools_result = await session.list_tools()
                print(f"✅ MCP connection successful!")
                print(f"Found {len(tools_result.tools)} tools:")
                
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                return True
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    print("🧪 Testing Gateway-Runtime Connection")
    print("=" * 50)
    
    success = asyncio.run(test_gateway_connection())
    
    if success:
        print("\n🎉 Gateway-Runtime connection is working!")
        print("✅ Phase 4 Gateway Integration completed successfully")
        print("\nNext: Test end-to-end agent workflow")
    else:
        print("\n❌ Gateway-Runtime connection still has issues")
        print("The Runtime may need additional configuration to work with Gateway")

if __name__ == "__main__":
    main()
