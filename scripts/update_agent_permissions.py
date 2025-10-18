#!/usr/bin/env python3
import boto3
import json

iam = boto3.client('iam')

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
            ]
        }
    ]
}

try:
    iam.put_role_policy(
        RoleName='BedrockAgentSecurityChatbotRole',
        PolicyName='BedrockModelAccess',
        PolicyDocument=json.dumps(policy)
    )
    print("✅ Updated IAM permissions for Claude 3 Haiku")
except Exception as e:
    print(f"❌ Error: {e}")
