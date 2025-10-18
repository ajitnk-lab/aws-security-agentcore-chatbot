#!/usr/bin/env python3
"""
AWS Security MCP Server for AgentCore Runtime
Transforms the existing MCP server to work with AgentCore Runtime
"""

import json
import os
from typing import Dict, Any

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from well_architected_security_mcp_server.server import mcp

# Initialize AgentCore Runtime App
app = BedrockAgentCoreApp()

@app.entrypoint
def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    AgentCore Runtime entrypoint for MCP server
    Handles incoming requests and routes them to MCP tools
    """
    
    try:
        # Extract the tool call information from the request
        tool_name = request.get('tool_name')
        arguments = request.get('arguments', {})
        
        # Map tool names to MCP server functions
        tool_mapping = {
            'CheckSecurityServices': 'check_security_services',
            'GetSecurityFindings': 'get_security_findings', 
            'CheckStorageEncryption': 'check_storage_encryption',
            'CheckNetworkSecurity': 'check_network_security',
            'ListServicesInRegion': 'list_services_in_region',
            'GetStoredSecurityContext': 'get_stored_security_context'
        }
        
        if tool_name not in tool_mapping:
            return {
                'error': f'Unknown tool: {tool_name}',
                'available_tools': list(tool_mapping.keys())
            }
        
        # Get the MCP function name
        mcp_function = tool_mapping[tool_name]
        
        # Execute the MCP tool
        if hasattr(mcp, mcp_function):
            result = getattr(mcp, mcp_function)(**arguments)
            return {
                'success': True,
                'tool_name': tool_name,
                'result': result
            }
        else:
            return {
                'error': f'MCP function not found: {mcp_function}',
                'tool_name': tool_name
            }
            
    except Exception as e:
        return {
            'error': str(e),
            'tool_name': tool_name if 'tool_name' in locals() else 'unknown'
        }

def list_available_tools() -> Dict[str, Any]:
    """List all available MCP tools and their descriptions"""
    return {
        'tools': [
            {
                'name': 'CheckSecurityServices',
                'description': 'Check if AWS security services are enabled',
                'parameters': {
                    'region': 'AWS region to check (optional)'
                }
            },
            {
                'name': 'GetSecurityFindings',
                'description': 'Get security findings from multiple AWS services',
                'parameters': {
                    'region': 'AWS region to check (optional)',
                    'severity': 'Filter by severity (HIGH, MEDIUM, LOW)'
                }
            },
            {
                'name': 'CheckStorageEncryption',
                'description': 'Check storage encryption compliance',
                'parameters': {
                    'region': 'AWS region to check (optional)'
                }
            },
            {
                'name': 'CheckNetworkSecurity',
                'description': 'Check network security configurations',
                'parameters': {
                    'region': 'AWS region to check (optional)'
                }
            },
            {
                'name': 'ListServicesInRegion',
                'description': 'List AWS services in use in a region',
                'parameters': {
                    'region': 'AWS region to check'
                }
            },
            {
                'name': 'GetStoredSecurityContext',
                'description': 'Get stored security context from previous assessments',
                'parameters': {
                    'context_id': 'Context identifier (optional)'
                }
            }
        ]
    }

if __name__ == "__main__":
    # Let AgentCore Runtime control the running of the agent
    app.run()
