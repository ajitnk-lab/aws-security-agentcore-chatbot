#!/usr/bin/env python3

import boto3
import json

def create_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Simple OpenAPI schema
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Security Tools API",
            "version": "1.0.0"
        },
        "paths": {
            "/security/status": {
                "get": {
                    "operationId": "get_security_status",
                    "summary": "Get security service status",
                    "responses": {
                        "200": {
                            "description": "Success"
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
            actionGroupName='security-tools',
            description='AWS Security analysis tools via AgentCore Gateway',
            actionGroupExecutor={
                'customControl': 'RETURN_CONTROL'
            },
            apiSchema={
                'payload': json.dumps(schema)
            }
        )
        
        print("Action Group created successfully!")
        print(f"Action Group ID: {response['agentActionGroup']['actionGroupId']}")
        return response
        
    except Exception as e:
        print(f"Error creating Action Group: {e}")
        return None

if __name__ == "__main__":
    create_action_group()
