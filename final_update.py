#!/usr/bin/env python3

import boto3
import json

def update_action_group():
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Minimal valid OpenAPI schema
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Security API",
            "version": "1.0.0"
        },
        "paths": {
            "/security": {
                "post": {
                    "operationId": "security_check",
                    "summary": "Security check",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Success",
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
    }
    
    try:
        response = client.update_agent_action_group(
            agentId='VS4IAMTUZO',
            agentVersion='DRAFT',
            actionGroupId='FVTIWFVSXE',
            actionGroupName='security-tools',
            description='Security tools via Lambda',
            actionGroupExecutor={
                'lambda': 'arn:aws:lambda:us-east-1:039920874011:function:bedrock-gateway-proxy'
            },
            apiSchema={
                'payload': json.dumps(schema)
            }
        )
        
        print("✅ Action Group updated successfully")
        print("🔄 Preparing agent...")
        
        client.prepare_agent(agentId='VS4IAMTUZO')
        print("✅ Agent prepared")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_action_group()
