#!/usr/bin/env python3

import boto3
import json

def create_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Load the minimal schema
    with open('minimal_schema.json', 'r') as f:
        schema = json.load(f)
    
    try:
        response = client.create_agent_action_group(
            agentId='VS4IAMTUZO',
            agentVersion='DRAFT',
            actionGroupName='security-tools',
            description='AWS Security Tools',
            actionGroupExecutor={
                'customControl': 'RETURN_CONTROL'
            },
            apiSchema={
                'payload': json.dumps(schema)
            }
        )
        
        print("✅ Action Group created successfully!")
        print(f"Action Group ID: {response['agentActionGroup']['actionGroupId']}")
        print(f"Action Group Name: {response['agentActionGroup']['actionGroupName']}")
        
        # Now prepare the agent
        print("\n🔄 Preparing agent...")
        prepare_response = client.prepare_agent(
            agentId='VS4IAMTUZO'
        )
        print(f"✅ Agent preparation status: {prepare_response['agentStatus']}")
        
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    create_action_group()
