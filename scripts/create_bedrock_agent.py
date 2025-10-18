#!/usr/bin/env python3
"""
Create Bedrock Agent with Claude 3.7 Sonnet for security analysis.
Task 5.1: Create Bedrock Agent with Claude 3.7 Sonnet
"""

import boto3
import json
import time
from datetime import datetime

def create_bedrock_agent():
    """Create Bedrock Agent with security analysis configuration"""
    
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Agent configuration
    agent_name = f"security-chatbot-agent-{int(time.time())}"
    
    # Security expert instructions
    instructions = """You are an AWS security expert assistant that helps analyze and improve AWS security posture.

Your capabilities:
- Analyze AWS security services status (GuardDuty, Security Hub, Inspector)
- Check storage encryption across S3, EBS, RDS
- Evaluate network security configurations
- Retrieve and analyze security findings
- Provide actionable security recommendations
- Discover AWS services in use across regions

Guidelines:
- Always provide specific, actionable recommendations
- Explain security risks in business terms
- Prioritize critical and high-severity findings
- Reference AWS Well-Architected Security Pillar best practices
- Be concise but thorough in your analysis
- Ask clarifying questions when needed

When users ask about security, use the available tools to gather current data before providing recommendations."""

    # Use the created IAM role
    role_arn = "arn:aws:iam::039920874011:role/BedrockAgentSecurityChatbotRole"

    try:
        print("🤖 Creating Bedrock Agent...")
        
        response = client.create_agent(
            agentName=agent_name,
            description="AWS Security Analysis Agent with AgentCore integration",
            foundationModel="anthropic.claude-3-7-sonnet-20250219-v1:0",
            instruction=instructions,
            idleSessionTTLInSeconds=1800,  # 30 minutes
            agentResourceRoleArn=role_arn
        )
        
        agent_id = response['agent']['agentId']
        agent_arn = response['agent']['agentArn']
        
        print(f"✅ Agent created successfully!")
        print(f"Agent ID: {agent_id}")
        print(f"Agent ARN: {agent_arn}")
        
        # Save configuration
        config = {
            "agent_id": agent_id,
            "agent_arn": agent_arn,
            "agent_name": agent_name,
            "model": "anthropic.claude-3-7-sonnet-20250219-v1:0",
            "role_arn": role_arn,
            "created_at": datetime.now().isoformat()
        }
        
        with open("bedrock_agent_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to: bedrock_agent_config.json")
        
        return config
        
    except Exception as e:
        print(f"❌ Error creating Bedrock Agent: {e}")
        return None

if __name__ == "__main__":
    create_bedrock_agent()
