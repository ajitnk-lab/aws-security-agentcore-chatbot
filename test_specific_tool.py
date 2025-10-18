#!/usr/bin/env python3

import boto3
import json

def test_agent():
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    try:
        response = client.invoke_agent(
            agentId='VS4IAMTUZO',
            agentAliasId='OUUY9MTH8E',
            sessionId=f'test-{int(__import__("time").time())}',
            inputText='Please list the available security tools'
        )
        
        print("Agent Response:")
        for event in response['completion']:
            if 'chunk' in event:
                if 'bytes' in event['chunk']:
                    print(event['chunk']['bytes'].decode('utf-8'), end='')
            elif 'returnControl' in event:
                print(f"\n🔄 RETURN_CONTROL: {json.dumps(event['returnControl'], indent=2)}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_agent()
