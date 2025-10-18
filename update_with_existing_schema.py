#!/usr/bin/env python3

import boto3

def update_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Use existing schema
    existing_schema = '{"openapi": "3.0.0", "info": {"title": "Security Tools", "version": "1.0.0", "description": "AWS Security Tools API"}, "paths": {"/tools/list": {"post": {"operationId": "list_tools", "summary": "List available security tools", "description": "Get a list of available AWS security analysis tools", "requestBody": {"required": false, "content": {"application/json": {"schema": {"type": "object", "properties": {}}}}}, "responses": {"200": {"description": "List of available tools", "content": {"application/json": {"schema": {"type": "object", "properties": {"tools": {"type": "array", "items": {"type": "string"}}}}}}}}}}}'
    
    try:
        response = client.update_agent_action_group(
            agentId='VS4IAMTUZO',
            agentVersion='DRAFT',
            actionGroupId='FVTIWFVSXE',
            actionGroupName='security-tools',
            description='AWS Security Tools via Lambda proxy',
            actionGroupExecutor={
                'lambda': 'arn:aws:lambda:us-east-1:039920874011:function:bedrock-gateway-proxy'
            },
            apiSchema={
                'payload': existing_schema
            }
        )
        
        print("✅ Action Group updated to use Lambda proxy")
        
        # Prepare agent
        client.prepare_agent(agentId='VS4IAMTUZO')
        print("✅ Agent prepared")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_action_group()
