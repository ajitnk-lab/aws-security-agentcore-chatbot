# 🔄 Resume AWS Security AgentCore Chatbot Project

**Copy and paste this prompt to resume work after crashes/context overflow:**

---

## 📋 Project Context

I'm working on deploying an AWS Security MCP Server on Amazon Bedrock AgentCore to create an intelligent security chatbot. The project is located at:

```
/persistent/home/ubuntu/workspace/aws-security-agentcore-chatbot
```

## 🎯 Project Overview

- **Goal**: Deploy existing AWS Well-Architected Security MCP Server on Bedrock AgentCore
- **Architecture**: Chat UI ↔ Bedrock Agent ↔ AgentCore Gateway ↔ MCP Server ↔ AWS Security Services
- **Components**: AgentCore Runtime, Memory, Gateway, Observability + CDK Infrastructure

## ✅ Completed Tasks

1. ✅ Created GitHub repository: `aws-security-agentcore-chatbot`
2. ✅ Project structure with docs (requirements.md, design.md, task.md)
3. ✅ CDK infrastructure setup with TypeScript
4. ✅ MCP server source code copied from existing project
5. ✅ AgentCore CLI installed globally (`agentcore --help` works)
6. ✅ All dependencies installed (bedrock-agentcore, starter-toolkit, strands-agents, mcp)

## 🔧 Current Status

**TODO List ID**: `1760766399107`

**Next Tasks**:
- [ ] Set up AWS credentials and permissions
- [ ] Create CDK infrastructure stack for AgentCore resources  
- [ ] Deploy AgentCore Memory resource with semantic strategies
- [ ] Deploy AgentCore Gateway with MCP server integration
- [ ] Package and deploy MCP server to AgentCore Runtime
- [ ] Create Bedrock Agent with tool integrations
- [ ] Implement chat interface for security assistant
- [ ] Test end-to-end security chatbot functionality

## 🛠️ Available Tools

- **AgentCore CLI**: `agentcore launch`, `agentcore configure`, `agentcore create_mcp_gateway`
- **MCP Server**: 6 security tools (CheckSecurityServices, GetSecurityFindings, etc.)
- **CDK**: Infrastructure as Code ready for deployment
- **GitHub**: https://github.com/ajitnk-lab/aws-security-agentcore-chatbot

## 🚀 Resume Instructions

1. Load the TODO list: `todo_list load 1760766399107`
2. Check current working directory: `cd /persistent/home/ubuntu/workspace/aws-security-agentcore-chatbot`
3. Continue with next incomplete task from the TODO list
4. Use AgentCore CLI and CDK tools as needed
5. Update TODO list as tasks are completed

## ⚡ CRITICAL WORKING METHODOLOGY

### 🏃‍♂️ **Startup Approach - FAIL FAST**
- **Code → Deploy → Test → Iterate** rapidly
- Don't over-engineer - get basic functionality working first
- Test early, fail fast, learn quickly
- Deploy frequently to catch issues early

### 🎯 **MVP-First Strategy**
1. **Build MVP with basic functionality FIRST**
2. **Get end-to-end flow working** (even if simple)
3. **Add features incrementally** one by one
4. **Test each feature** before adding the next

### 📝 **Continuous Documentation**
- **Update task.md** after every major milestone
- **Update TODO list** as tasks complete/change
- **Commit to GitHub** frequently with meaningful messages
- **Document learnings** and blockers immediately

### 🔬 **Detailed Task Management**
- **Break down tasks** into 15-30 minute chunks
- **Create minute-level task items** for complex work
- **Track progress** granularly to avoid losing work
- **Update estimates** based on actual time taken

### 🏗️ **CRITICAL: ARCHITECTURE INTEGRITY**
- **NEVER deviate** from original architecture/design/flow
- **NO workarounds** or quick fixes that bypass proper flow
- **NO mock-ups**, static returns, or fake data
- **NO shortcuts** that compromise the intended architecture
- **ALWAYS implement** the real Chat UI ↔ Agent ↔ Gateway ↔ MCP ↔ AWS flow
- **FAIL PROPERLY** rather than fake success

### 🏆 **AWS BEST PRACTICES - ALWAYS**
- **Never rush** - Quality over speed, even under pressure
- **Code over docs** - Trust working code, verify with tests
- **AWS Well-Architected** - Security, reliability, performance
- **Least privilege IAM** - Minimal permissions for each component
- **Infrastructure as Code** - CDK for all resources
- **Proper monitoring** - CloudWatch metrics and alarms

## 📁 Key Files

- `docs/requirements.md` - Detailed project requirements
- `docs/design.md` - System architecture and design
- `docs/task.md` - 20-day implementation roadmap
- `infrastructure/bin/app.ts` - CDK application entry point
- `src/mcp-server/` - Security MCP server source code
- `package.json` - Node.js dependencies and scripts

**Ready to continue implementation!** 🎯
