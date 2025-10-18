#!/usr/bin/env python3

import os
import re

def fix_imports_in_file(filepath):
    """Fix awslabs imports in a Python file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace awslabs.well_architected_security_mcp_server imports
    # Pattern 1: from awslabs.well_architected_security_mcp_server import X
    content = re.sub(
        r'from awslabs\.well_architected_security_mcp_server import',
        'from agentcore_mcp_server import',
        content
    )
    
    # Pattern 2: from awslabs.well_architected_security_mcp_server.X import Y
    content = re.sub(
        r'from awslabs\.well_architected_security_mcp_server\.([^.\s]+)',
        r'from agentcore_mcp_server.\1',
        content
    )
    
    # Pattern 3: import awslabs.well_architected_security_mcp_server.X
    content = re.sub(
        r'import awslabs\.well_architected_security_mcp_server\.([^.\s]+)',
        r'import agentcore_mcp_server.\1',
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Fixed imports in {filepath}")

# Fix imports in all Python files
base_dir = "/persistent/home/ubuntu/workspace/aws-security-agentcore-chatbot/src/mcp-server/agentcore_mcp_server"
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            fix_imports_in_file(filepath)

print("All imports fixed!")
