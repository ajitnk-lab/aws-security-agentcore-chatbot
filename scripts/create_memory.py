#!/usr/bin/env python3
"""
Create AgentCore Memory Resource for Security Chatbot
"""

from bedrock_agentcore_starter_toolkit.operations.memory.manager import MemoryManager
from bedrock_agentcore_starter_toolkit.operations.memory.models.strategies import SemanticStrategy
import json

def create_security_memory():
    """Create AgentCore Memory resource with semantic strategy"""
    
    # Initialize memory manager for us-east-1
    memory_manager = MemoryManager(region_name="us-east-1")
    
    print("Creating AgentCore Memory resource for security chatbot...")
    
    # Create memory resource with semantic strategy
    memory = memory_manager.get_or_create_memory(
        name="SecurityChatbotMemory",
        description="Memory store for AWS security chatbot conversations and insights",
        strategies=[
            SemanticStrategy(
                name="securitySemanticMemory",
                namespaces=['/strategies/{memoryStrategyId}/actors/{actorId}'],
            )
        ]
    )
    
    memory_id = memory.get('id')
    print(f"✅ Memory resource created successfully!")
    print(f"Memory ID: {memory_id}")
    
    # Save memory ID to file for later use
    with open('memory_config.json', 'w') as f:
        json.dump({
            'memory_id': memory_id,
            'name': 'SecurityChatbotMemory',
            'region': 'us-east-1',
            'strategies': ['securitySemanticMemory']
        }, f, indent=2)
    
    print("Memory configuration saved to memory_config.json")
    
    # List all memories to verify
    memories = memory_manager.list_memories()
    print(f"\nTotal memories in account: {len(memories)}")
    
    return memory_id

if __name__ == "__main__":
    memory_id = create_security_memory()
    print(f"\n🎯 Next steps:")
    print(f"1. Use memory_id: {memory_id}")
    print(f"2. Test memory operations")
    print(f"3. Configure semantic extraction strategies")
