#!/usr/bin/env python3
"""
Set up IAM permissions for Bedrock Agent creation and operation.
"""

import boto3
import json

def create_bedrock_agent_role():
    """Create IAM role for Bedrock Agent"""
    
    iam = boto3.client('iam', region_name='us-east-1')
    
    # Trust policy for Bedrock Agent
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "bedrock.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    # Permissions policy
    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-7-sonnet-20250219-v1:0"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock-agentcore:InvokeAgentRuntime",
                    "bedrock-agentcore:GetWorkloadAccessToken"
                ],
                "Resource": "*"
            }
        ]
    }
    
    role_name = "BedrockAgentSecurityChatbotRole"
    
    try:
        print("🔐 Creating Bedrock Agent IAM role...")
        
        # Create role
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="IAM role for Security Chatbot Bedrock Agent"
        )
        
        role_arn = role_response['Role']['Arn']
        print(f"✅ Role created: {role_arn}")
        
        # Create and attach policy
        policy_name = "BedrockAgentSecurityChatbotPolicy"
        
        policy_response = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(permissions_policy),
            Description="Permissions for Security Chatbot Bedrock Agent"
        )
        
        policy_arn = policy_response['Policy']['Arn']
        print(f"✅ Policy created: {policy_arn}")
        
        # Attach policy to role
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        
        print("✅ Policy attached to role")
        
        return role_arn
        
    except iam.exceptions.EntityAlreadyExistsException:
        print("ℹ️  Role already exists, getting ARN...")
        role_response = iam.get_role(RoleName=role_name)
        return role_response['Role']['Arn']
        
    except Exception as e:
        print(f"❌ Error creating role: {e}")
        return None

if __name__ == "__main__":
    role_arn = create_bedrock_agent_role()
    if role_arn:
        print(f"\n🎯 Use this role ARN for Bedrock Agent: {role_arn}")
