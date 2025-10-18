#!/usr/bin/env python3
"""
Example External Security Agent

This demonstrates how external agents can connect to our AgentCore Gateway
to access security tools via MCP protocol.
"""

import json
import asyncio
import httpx
from datetime import datetime, timedelta

class SecurityAgent:
    """External security agent that uses AgentCore Gateway"""
    
    def __init__(self, gateway_config_file="gateway_config.json"):
        # Load gateway configuration
        with open(gateway_config_file, "r") as f:
            self.config = json.load(f)
        
        # Initialize token manager
        self.token_manager = GatewayTokenManager(
            client_id=self.config['client_id'],
            client_secret=self.config['client_secret'],
            token_endpoint=self.config['token_endpoint'],
            scope=self.config['scope']
        )
        
        self.gateway_url = self.config['gateway_url']
    
    async def call_tool(self, tool_name, arguments):
        """Call a security tool through the Gateway"""
        token = await self.token_manager.get_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.gateway_url,
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
            
            result = response.json()
            if 'error' in result:
                raise Exception(f"Tool error: {result['error']}")
            
            return result.get('result')
    
    async def security_assessment(self, region="us-east-1"):
        """Perform comprehensive security assessment"""
        print(f"🔍 Starting security assessment for region: {region}")
        
        # Check security services status
        print("\n1️⃣ Checking security services...")
        services_status = await self.call_tool("CheckSecurityServices", {"region": region})
        print(f"Security Services: {services_status}")
        
        # Get security findings
        print("\n2️⃣ Retrieving security findings...")
        findings = await self.call_tool("GetSecurityFindings", {"region": region})
        print(f"Security Findings: {len(findings.get('findings', []))} found")
        
        # Check storage encryption
        print("\n3️⃣ Checking storage encryption...")
        encryption_status = await self.call_tool("CheckStorageEncryption", {"region": region})
        print(f"Encryption Status: {encryption_status}")
        
        # Check network security
        print("\n4️⃣ Analyzing network security...")
        network_security = await self.call_tool("CheckNetworkSecurity", {"region": region})
        print(f"Network Security: {network_security}")
        
        # List services in region
        print("\n5️⃣ Listing services in region...")
        services = await self.call_tool("ListServicesInRegion", {"region": region})
        print(f"Services in Region: {len(services.get('services', []))} services")
        
        return {
            "region": region,
            "services_status": services_status,
            "findings": findings,
            "encryption_status": encryption_status,
            "network_security": network_security,
            "services": services
        }
    
    async def process_user_query(self, query):
        """Process natural language security queries"""
        query_lower = query.lower()
        
        if "security status" in query_lower or "security overview" in query_lower:
            return await self.security_assessment()
        
        elif "encryption" in query_lower:
            result = await self.call_tool("CheckStorageEncryption", {"region": "us-east-1"})
            return f"Encryption Status: {result}"
        
        elif "findings" in query_lower or "vulnerabilities" in query_lower:
            result = await self.call_tool("GetSecurityFindings", {"region": "us-east-1"})
            return f"Security Findings: {len(result.get('findings', []))} issues found"
        
        elif "network" in query_lower:
            result = await self.call_tool("CheckNetworkSecurity", {"region": "us-east-1"})
            return f"Network Security: {result}"
        
        elif "services" in query_lower:
            result = await self.call_tool("ListServicesInRegion", {"region": "us-east-1"})
            return f"Services: {len(result.get('services', []))} services in region"
        
        else:
            return "I can help with: security status, encryption, findings, network security, or services. What would you like to know?"

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
            
            data = response.json()
            self._token = data['access_token']
            expires_in = data.get('expires_in', 3600) - 300
            self._expires_at = datetime.now() + timedelta(seconds=expires_in)
            return self._token

async def main():
    """Demo the external security agent"""
    print("🤖 AWS Security Agent Demo")
    print("=" * 50)
    
    try:
        agent = SecurityAgent()
        
        # Demo queries
        queries = [
            "What's my security status?",
            "Check encryption status",
            "Show me security findings",
            "Analyze network security"
        ]
        
        for query in queries:
            print(f"\n👤 User: {query}")
            response = await agent.process_user_query(query)
            print(f"🤖 Agent: {response}")
            print("-" * 30)
        
        # Full assessment
        print(f"\n🔍 Full Security Assessment:")
        assessment = await agent.security_assessment()
        print(json.dumps(assessment, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
