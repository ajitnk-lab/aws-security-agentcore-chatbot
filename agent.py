#!/usr/bin/env python3
"""
AWS Security AgentCore Chatbot - Main Agent Entry Point
"""

from bedrock_agentcore import Agent

def create_agent():
    """Create and configure the security chatbot agent"""
    agent = Agent(
        name="aws-security-chatbot",
        description="Intelligent AWS security assistant with real-time insights",
        model="anthropic.claude-3-7-sonnet-20250219-v1:0",
        instructions="""
        You are an AWS security expert assistant. You help users:
        - Check AWS security service status
        - Analyze security findings
        - Validate compliance configurations
        - Provide security recommendations
        
        Use the available MCP tools to gather real-time AWS security data.
        Always provide actionable insights and follow AWS Well-Architected principles.
        """
    )
    
    return agent

if __name__ == "__main__":
    agent = create_agent()
    print("AWS Security AgentCore Chatbot initialized")
