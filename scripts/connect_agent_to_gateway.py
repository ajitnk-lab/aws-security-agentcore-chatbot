#!/usr/bin/env python3
"""
Connect Bedrock Agent to AgentCore Gateway.
Tasks 5.3: Connect agent to AgentCore Gateway (OAuth flow)
"""

import boto3
import json
import time

def connect_agent_to_gateway():
    """Connect Bedrock Agent to AgentCore Gateway"""
    
    # Load configurations
    try:
        with open("bedrock_agent_config.json", "r") as f:
            agent_config = json.load(f)
        with open("gateway_config.json", "r") as f:
            gateway_config = json.load(f)
    except FileNotFoundError as e:
        print(f"❌ Configuration file not found: {e}")
        return None
    
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    agent_id = agent_config['agent_id']
    
    print(f"🔗 Connecting Agent {agent_id} to Gateway...")
    
    try:
        # Create action group for Gateway integration
        action_group_response = client.create_agent_action_group(
            agentId=agent_id,
            agentVersion='DRAFT',
            actionGroupName='SecurityToolsActionGroup',
            description='AWS Security Tools via AgentCore Gateway',
            actionGroupExecutor={
                'customControl': 'RETURN_CONTROL'
            },
            apiSchema={
                'payload': json.dumps({
                    "openapi": "3.0.0",
                    "info": {
                        "title": "Security Tools API",
                        "version": "1.0.0"
                    },
                    "paths": {
                        "/security/check-services": {
                            "post": {
                                "operationId": "checkSecurityServices",
                                "summary": "Check AWS security services status",
                                "requestBody": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "region": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                },
                                "responses": {"200": {"description": "Success"}}
                            }
                        },
                        "/security/check-encryption": {
                            "post": {
                                "operationId": "checkStorageEncryption",
                                "summary": "Check storage encryption status",
                                "requestBody": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "region": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                },
                                "responses": {"200": {"description": "Success"}}
                            }
                        }
                    }
                })
            }
        )
        
        action_group_id = action_group_response['agentActionGroup']['actionGroupId']
        print(f"✅ Action Group created: {action_group_id}")
        
        # Prepare and create agent version
        print("📦 Preparing Agent...")
        client.prepare_agent(agentId=agent_id)
        
        # Wait for preparation
        time.sleep(10)
        
        # Create agent alias
        alias_response = client.create_agent_alias(
            agentId=agent_id,
            agentAliasName='SecurityChatbotAlias',
            description='Production alias for Security Chatbot Agent'
        )
        
        alias_id = alias_response['agentAlias']['agentAliasId']
        alias_arn = alias_response['agentAlias']['agentAliasArn']
        
        print(f"✅ Agent Alias created: {alias_id}")
        print(f"Agent Alias ARN: {alias_arn}")
        
        # Update configuration
        agent_config.update({
            "action_group_id": action_group_id,
            "alias_id": alias_id,
            "alias_arn": alias_arn,
            "gateway_url": gateway_config["gateway_url"],
            "status": "connected"
        })
        
        with open("bedrock_agent_config.json", "w") as f:
            json.dump(agent_config, f, indent=2)
        
        print("✅ Agent connected to Gateway successfully!")
        return agent_config
        
    except Exception as e:
        print(f"❌ Error connecting agent to gateway: {e}")
        return None

if __name__ == "__main__":
    connect_agent_to_gateway()
