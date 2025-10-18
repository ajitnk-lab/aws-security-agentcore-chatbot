# AWS Security AgentCore Chatbot - Actual Deployment Flow

## 🔄 **COMPLETE FLOW FROM UI TO MCP TOOLS**

### **1. Frontend (UI)**
- **S3 Bucket**: `aws-security-chatbot-ui-2024`
- **Website URL**: `http://aws-security-chatbot-ui-2024.s3-website-us-east-1.amazonaws.com`
- **Technology**: React app with static hosting

### **2. API Gateway**
- **API Gateway ID**: `hinh3actqf`
- **API Name**: `chatbot-api`
- **Endpoint**: `https://hinh3actqf.execute-api.us-east-1.amazonaws.com/prod/chat`
- **Method**: POST to `/chat`

### **3. Web API Lambda**
- **Function Name**: `chatbot-web-api`
- **Function ARN**: `arn:aws:lambda:us-east-1:039920874011:function:chatbot-web-api`
- **Runtime**: Python 3.9
- **Role**: `GatewayProxyLambdaRole`

### **4. Bedrock Agent**
- **Agent ID**: `VS4IAMTUZO`
- **Agent Name**: `security-chatbot-agent`
- **Agent ARN**: `arn:aws:bedrock:us-east-1:039920874011:agent/VS4IAMTUZO`
- **Alias ID**: `OUUY9MTH8E`
- **Foundation Model**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Status**: PREPARED

### **5. Agent Action Group**
- **Action Group ID**: `1B3RBFLIEZ`
- **Action Group Name**: `security-lambda`
- **State**: ENABLED
- **Functions**: 5 security tools
  - `get_security_status`
  - `get_security_findings`
  - `check_storage_encryption`
  - `list_services_in_region`
  - `check_network_security`

### **6. Security Lambda (Tool Executor)**
- **Function Name**: `bedrock-gateway-proxy`
- **Function ARN**: `arn:aws:lambda:us-east-1:039920874011:function:bedrock-gateway-proxy`
- **Runtime**: Python 3.9
- **Role**: `GatewayProxyLambdaRole`

### **7. AgentCore Gateway (Available but not in active flow)**
- **Gateway URL**: `https://security-chatbot-gateway-41f3cc60-fmqz5lmy6j.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp`
- **Gateway ID**: `security-chatbot-gateway-41f3cc60-fmqz5lmy6j`
- **OAuth Client ID**: `6aarhftf6bopppar05humcp2r6`

### **8. AgentCore Runtime (Available but not in active flow)**
- **Runtime ARN**: `arn:aws:bedrock-agentcore:us-east-1:039920874011:runtime/agentcore_mcp_server-CmiD0a32zF`
- **Endpoint**: `https://agentcore_mcp_server-CmiD0a32zF.runtime.bedrock-agentcore.us-east-1.amazonaws.com`

### **9. MCP Server Tools (Available but not in active flow)**
- **Available Tools**: 6 security tools with prefix `SecurityMCPTools___`
- **Tools**: CheckSecurityServices, GetSecurityFindings, CheckStorageEncryption, ListServicesInRegion, CheckNetworkSecurity, GetStoredSecurityContext

## 📊 **ACTUAL ACTIVE FLOW PATH**

```
User Input
    ↓
S3 Website (aws-security-chatbot-ui-2024)
    ↓
API Gateway (hinh3actqf) → /prod/chat
    ↓
Web API Lambda (chatbot-web-api)
    ↓
Bedrock Agent (VS4IAMTUZO/OUUY9MTH8E)
    ↓
Agent Action Group (security-lambda/1B3RBFLIEZ)
    ↓
Security Lambda (bedrock-gateway-proxy)
    ↓
Direct AWS API Calls (GuardDuty, Security Hub, S3, EC2, etc.)
    ↓
Security Analysis Response
```

## ⚠️ **IMPORTANT NOTES**

1. **Current Implementation**: Uses **direct Lambda approach** where `bedrock-gateway-proxy` directly calls AWS security APIs
2. **AgentCore Components**: Deployed but **NOT in active flow path**
3. **Security Tools**: 5 working tools providing real Security Hub findings and ratings
4. **Status**: **FULLY FUNCTIONAL** - provides actual security ratings (A+ to D) based on Security Hub findings

## 🛡️ **Working Security Features**

- ✅ Real Security Hub findings analysis
- ✅ Security rating calculation (A+ to D)
- ✅ GuardDuty status checking
- ✅ Storage encryption analysis
- ✅ Network security assessment
- ✅ AWS services inventory

## 🌐 **Access Points**

- **Website**: http://aws-security-chatbot-ui-2024.s3-website-us-east-1.amazonaws.com
- **API**: https://hinh3actqf.execute-api.us-east-1.amazonaws.com/prod/chat

---
*Last Updated: 2025-10-18*
