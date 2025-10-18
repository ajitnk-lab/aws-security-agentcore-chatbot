#!/usr/bin/env python3
"""
Deploy AgentCore Runtime programmatically
"""
import subprocess
import os

def deploy_runtime():
    print("🚀 Deploying AgentCore Runtime...")
    
    # Create .bedrock_agentcore.yaml config file
    config = """
agents:
  security_agent:
    entrypoint: agent.py
    requirements: requirements.txt
    name: security_agent
    runtime:
      name: agentcore_mcp_server-development
"""
    
    with open('.bedrock_agentcore.yaml', 'w') as f:
        f.write(config)
    
    print("✅ Configuration created")
    
    # Launch the runtime
    try:
        result = subprocess.run(['agentcore', 'launch'], 
                              capture_output=True, text=True, timeout=300)
        print(f"Launch output: {result.stdout}")
        if result.stderr:
            print(f"Launch errors: {result.stderr}")
        
        if result.returncode == 0:
            print("✅ Runtime deployed successfully!")
        else:
            print(f"❌ Runtime deployment failed with code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("❌ Runtime deployment timed out")
    except Exception as e:
        print(f"❌ Runtime deployment error: {e}")

if __name__ == "__main__":
    deploy_runtime()
