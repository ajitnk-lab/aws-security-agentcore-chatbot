#!/usr/bin/env python3
"""
Add Action Group to Bedrock Agent to connect to AgentCore Gateway
"""
import boto3
import json

def add_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Load gateway configuration
    with open('gateway_config.json', 'r') as f:
        gateway_config = json.load(f)
    
    gateway_url = gateway_config['gateway_url']
    
    # Create Action Group with Lambda function that calls Gateway
    response = client.create_agent_action_group(
        agentId='VS4IAMTUZO',
        agentVersion='DRAFT',
        actionGroupName='SecurityTools',
        description='AWS Security analysis tools via AgentCore Gateway',
        actionGroupExecutor={
            'lambda': 'arn:aws:lambda:us-east-1:039920874011:function:security-gateway-proxy'
        },
        apiSchema={
            'payload': json.dumps({
                "openapi": "3.0.0",
                "info": {
                    "title": "Security Tools API",
                    "version": "1.0.0"
                },
                "paths": {
                    "/check-security-status": {
                        "post": {
                            "operationId": "checkSecurityStatus",
                            "summary": "Check AWS security services status",
                            "requestBody": {
                                "required": False,
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {}
                                        }
                                    }
                                }
                            },
                            "responses": {
                                "200": {
                                    "description": "Security services status",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            })
        }
    )
    
    print(f"✅ Action Group created: {response['agentActionGroup']['actionGroupId']}")
    return response

if __name__ == "__main__":
    add_action_group()
