#!/usr/bin/env python3

import boto3
import json

def create_lambda_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Simple valid schema
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Security Tools",
            "version": "1.0.0"
        },
        "paths": {
            "/security": {
                "get": {
                    "operationId": "get_security_status",
                    "summary": "Get security status",
                    "responses": {
                        "200": {
                            "description": "Security status"
                        }
                    }
                }
            }
        }
    }
    
    try:
        response = client.create_agent_action_group(
            agentId='VS4IAMTUZO',
            agentVersion='DRAFT',
            actionGroupName='security-lambda-tools',
            description='Security tools via Lambda proxy',
            actionGroupExecutor={
                'lambda': 'arn:aws:lambda:us-east-1:039920874011:function:bedrock-gateway-proxy'
            },
            apiSchema={
                'payload': json.dumps(schema)
            }
        )
        
        print("✅ Lambda Action Group created")
        print(f"Action Group ID: {response['agentActionGroup']['actionGroupId']}")
        
        # Prepare agent
        client.prepare_agent(agentId='VS4IAMTUZO')
        print("✅ Agent prepared")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_lambda_action_group()
