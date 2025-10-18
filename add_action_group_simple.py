#!/usr/bin/env python3
"""
Add Action Group to Bedrock Agent to call the working Gateway
"""
import boto3
import json

def add_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Simple Action Group that calls the working Gateway
    response = client.create_agent_action_group(
        agentId='VS4IAMTUZO',
        agentVersion='DRAFT',
        actionGroupName='SecurityAnalysis',
        description='Security analysis tools via AgentCore Gateway',
        actionGroupExecutor={
            'customControl': 'RETURN_CONTROL'
        },
        apiSchema={
            'payload': json.dumps({
                "openapi": "3.0.0",
                "info": {"title": "Security API", "version": "1.0.0"},
                "paths": {
                    "/security-status": {
                        "post": {
                            "operationId": "getSecurityStatus",
                            "summary": "Get AWS security status",
                            "responses": {"200": {"description": "Success"}}
                        }
                    }
                }
            })
        }
    )
    
    print(f"✅ Action Group created: {response['agentActionGroup']['actionGroupId']}")
    
    # Prepare agent
    client.prepare_agent(agentId='VS4IAMTUZO')
    print("✅ Agent prepared")

if __name__ == "__main__":
    add_action_group()
