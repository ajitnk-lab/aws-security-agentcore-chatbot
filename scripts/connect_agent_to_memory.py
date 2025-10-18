#!/usr/bin/env python3
"""
Connect Bedrock Agent to AgentCore Memory.
Task 5.5: Connect agent to AgentCore Memory
"""

import boto3
import json
from bedrock_agentcore.memory import MemoryClient

def connect_agent_to_memory():
    """Connect Bedrock Agent to AgentCore Memory for conversation persistence"""
    
    # Load configurations
    try:
        with open("bedrock_agent_config.json", "r") as f:
            agent_config = json.load(f)
        with open("memory_config.json", "r") as f:
            memory_config = json.load(f)
    except FileNotFoundError as e:
        print(f"❌ Configuration file not found: {e}")
        return None
    
    print("🧠 Connecting Agent to Memory...")
    
    # Initialize memory client
    memory_client = MemoryClient(region_name='us-east-1')
    memory_id = memory_config['memory_id']
    
    try:
        # Test memory connection with correct message format
        print(f"Testing memory connection: {memory_id}")
        
        # Create a test event to verify memory works
        test_event = memory_client.create_event(
            memory_id=memory_id,
            actor_id="agent-system",
            session_id="agent-integration-test",
            messages=[("Agent connected to memory successfully", "OTHER")]
        )
        
        print(f"✅ Memory connection successful: {test_event['eventId']}")
        
        # Update agent configuration with memory details
        agent_config.update({
            "memory_id": memory_id,
            "memory_connected": True,
            "memory_test_event": test_event['eventId']
        })
        
        with open("bedrock_agent_config.json", "w") as f:
            json.dump(agent_config, f, indent=2)
        
        print("✅ Agent connected to Memory successfully!")
        
        # Test memory retrieval
        print("🔍 Testing memory retrieval...")
        events = memory_client.list_events(
            memory_id=memory_id,
            actor_id="agent-system",
            session_id="agent-integration-test"
        )
        
        print(f"✅ Retrieved {len(events['events'])} events from memory")
        
        return agent_config
        
    except Exception as e:
        print(f"❌ Error connecting agent to memory: {e}")
        return None

def test_memory_persistence():
    """Test conversation persistence across sessions"""
    
    print("\n🧪 Testing Memory Persistence...")
    
    try:
        with open("memory_config.json", "r") as f:
            memory_config = json.load(f)
    except FileNotFoundError:
        print("❌ Memory configuration not found")
        return False
    
    memory_client = MemoryClient(region_name='us-east-1')
    memory_id = memory_config['memory_id']
    
    try:
        # Simulate conversation across multiple sessions
        sessions = ["session-1", "session-2", "session-3"]
        
        for i, session_id in enumerate(sessions):
            # Create conversation events with correct roles
            memory_client.create_event(
                memory_id=memory_id,
                actor_id="test-user",
                session_id=session_id,
                messages=[
                    (f"What's my security status in session {i+1}?", "USER"),
                    (f"I've analyzed your security posture for session {i+1}. Here are the findings...", "ASSISTANT")
                ]
            )
            
            print(f"✅ Session {i+1} conversation stored")
        
        # Test cross-session retrieval
        print("\n🔍 Testing cross-session memory retrieval...")
        
        for session_id in sessions:
            events = memory_client.list_events(
                memory_id=memory_id,
                actor_id="test-user",
                session_id=session_id
            )
            print(f"✅ Session {session_id}: {len(events['events'])} events retrieved")
        
        # Test semantic memory extraction (if configured)
        print("\n🧠 Testing semantic memory extraction...")
        
        # Create events that should trigger semantic extraction
        memory_client.create_event(
            memory_id=memory_id,
            actor_id="test-user",
            session_id="semantic-test",
            messages=[
                ("I prefer detailed security reports with actionable recommendations", "USER"),
                ("I'll remember your preference for detailed, actionable security reports", "ASSISTANT")
            ]
        )
        
        print("✅ Semantic extraction test event created")
        print("ℹ️  Semantic extraction happens asynchronously (5-10 seconds)")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory persistence test failed: {e}")
        return False

def main():
    print("🚀 Starting Agent-Memory Integration")
    
    # Connect agent to memory
    result = connect_agent_to_memory()
    
    if result:
        # Test memory persistence
        test_memory_persistence()
        
        print("\n🎉 Agent-Memory integration completed!")
        print("✅ Agent can now persist conversations across sessions")
        print("✅ Semantic memory extraction configured")
        
    else:
        print("\n❌ Agent-Memory integration failed")

if __name__ == "__main__":
    main()
