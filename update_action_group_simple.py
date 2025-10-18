#!/usr/bin/env python3

import boto3

def update_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    try:
        response = client.update_agent_action_group(
            agentId='VS4IAMTUZO',
            agentVersion='DRAFT',
            actionGroupId='FVTIWFVSXE',
            actionGroupName='security-tools',
            actionGroupExecutor={
                'lambda': 'arn:aws:lambda:us-east-1:039920874011:function:bedrock-gateway-proxy'
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
