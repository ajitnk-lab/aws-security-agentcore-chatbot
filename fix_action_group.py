#!/usr/bin/env python3

import boto3
import json

def fix_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Delete existing Action Group
    try:
        client.update_agent_action_group(
            agentId='VS4IAMTUZO',
            agentVersion='DRAFT',
            actionGroupId='FVTIWFVSXE',
            actionGroupName='security-tools',
            actionGroupState='DISABLED',
            actionGroupExecutor={'customControl': 'RETURN_CONTROL'},
            apiSchema={'payload': '{"openapi": "3.0.0", "info": {"title": "Security Tools", "version": "1.0.0"}, "paths": {"/tools/list": {"post": {"operationId": "list_tools", "summary": "List tools", "responses": {"200": {"description": "Success"}}}}}}'}
        )
        print("✅ Disabled Action Group")
        
        client.delete_agent_action_group(
            agentId='VS4IAMTUZO',
            agentVersion='DRAFT',
            actionGroupId='FVTIWFVSXE'
        )
        print("✅ Deleted Action Group")
    except Exception as e:
        print(f"Delete error: {e}")
    
    # Create new one with Lambda
    try:
        response = client.create_agent_action_group(
            agentId='VS4IAMTUZO',
            agentVersion='DRAFT',
            actionGroupName='security-lambda',
            description='Security tools via Lambda',
            actionGroupExecutor={
                'lambda': 'arn:aws:lambda:us-east-1:039920874011:function:bedrock-gateway-proxy'
            },
            functionSchema={
                'functions': [
                    {
                        'name': 'get_security_status',
                        'description': 'Get AWS security service status'
                    }
                ]
            }
        )
        
        print("✅ Created Lambda Action Group")
        print(f"ID: {response['agentActionGroup']['actionGroupId']}")
        
        # Prepare agent
        client.prepare_agent(agentId='VS4IAMTUZO')
        print("✅ Agent prepared")
        
    except Exception as e:
        print(f"❌ Create error: {e}")

if __name__ == "__main__":
    fix_action_group()
