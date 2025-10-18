#!/usr/bin/env python3
"""
Test chat interface with real Bedrock Agent integration.
"""

import boto3
import json
import uuid
import time

def test_bedrock_agent_chat():
    """Test direct Bedrock Agent invocation"""
    
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'VS4IAMTUZO'
    agent_alias_id = 'OUUY9MTH8E'  # Updated with real alias
    session_id = f"test-{uuid.uuid4()}"
    
    test_messages = [
        "Hello, what can you help me with?",
        "What is my AWS security status?",
        "Check my storage encryption"
    ]
    
    print(f"🤖 Testing Bedrock Agent: {agent_id}")
    print(f"🔗 Using Alias: {agent_alias_id}")
    
    for message in test_messages:
        print(f"\n👤 User: {message}")
        
        try:
            response = client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=message
            )
            
            # Process streaming response
            assistant_response = ""
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        assistant_response += chunk['bytes'].decode('utf-8')
            
            print(f"🤖 Assistant: {assistant_response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            if "CREATING" in str(e):
                print("ℹ️  Agent alias is still being created, waiting...")
                time.sleep(10)

if __name__ == "__main__":
    test_bedrock_agent_chat()
