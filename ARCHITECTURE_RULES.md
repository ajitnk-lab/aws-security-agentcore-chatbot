# 🏗️ Architecture Integrity Rules - NON-NEGOTIABLE

## 🎯 Sacred Architecture Flow

```
Chat UI ↔ Bedrock Agent ↔ AgentCore Gateway ↔ MCP Server ↔ AWS Security Services
           ↕                    ↕
    AgentCore Memory    AgentCore Runtime
```

## ❌ FORBIDDEN PRACTICES

### Never Do These:
- **Mock Data**: No fake AWS responses or static security data
- **Workarounds**: No bypassing Gateway, Memory, or Runtime
- **Quick Fixes**: No shortcuts that break the intended flow
- **Static Returns**: No hardcoded responses instead of real AWS calls
- **Architecture Deviation**: No changing the core component flow
- **Fake Success**: No masking failures with fake positive responses

### Examples of What NOT to Do:
```python
# ❌ WRONG - Mock data
def get_security_status():
    return {"status": "all good", "fake": True}

# ❌ WRONG - Bypass gateway
agent.call_mcp_directly()

# ❌ WRONG - Skip memory
def chat_without_memory():
    return "I don't remember anything"
```

## ✅ REQUIRED PRACTICES

### Always Do These:
- **Real AWS Calls**: Every security check must hit actual AWS APIs
- **Proper Flow**: All requests must go through the complete stack
- **Authentic Responses**: Return actual AWS security service data
- **Error Handling**: Fail gracefully but fail authentically
- **Component Integration**: Use all AgentCore components as designed

### Examples of Correct Implementation:
```python
# ✅ CORRECT - Real AWS integration
def get_security_status():
    return guardduty_client.get_detector_status()

# ✅ CORRECT - Proper flow
user_query → agent → gateway → mcp_server → aws_apis

# ✅ CORRECT - Real memory usage
memory.store_conversation(user_input, agent_response)
```

## 🔍 Quality Gates

### Before Marking Any Task Complete:
1. **Real Data Check**: Verify responses contain actual AWS data
2. **Flow Verification**: Confirm request went through all components
3. **No Shortcuts**: Ensure no components were bypassed
4. **Authentic Errors**: Verify failures are real, not masked
5. **Architecture Compliance**: Confirm design pattern followed

## 🚨 When Things Break

### Proper Response to Issues:
- **Debug the real problem** - don't mask it
- **Fix the actual component** - don't bypass it
- **Maintain architecture integrity** - even if it takes longer
- **Document real blockers** - don't hide complexity
- **Ask for help** - don't fake solutions

### Never Do This When Stuck:
- Return fake data to "make it work"
- Skip components to "simplify"
- Mock responses to "show progress"
- Hardcode values to "demonstrate functionality"

## 🎯 Success Definition

**Real Success**: User gets actual AWS security data through the complete AgentCore stack

**Fake Success**: User gets any response that isn't from real AWS services through real components

## 📝 Commitment

**I commit to maintaining architecture integrity over speed, real functionality over fake demos, and authentic implementation over shortcuts.**

## 🏆 AWS Best Practices - ALWAYS

### Security & Compliance:
- **Least Privilege IAM**: Minimal permissions for each component
- **Encryption**: Data encrypted at rest and in transit
- **VPC Security**: Proper security groups and NACLs
- **Secrets Management**: Use AWS Secrets Manager, never hardcode
- **Audit Logging**: CloudTrail for all API calls

### Operational Excellence:
- **Infrastructure as Code**: CDK for all resources
- **Monitoring**: CloudWatch metrics and alarms
- **Tagging**: Consistent resource tagging strategy
- **Cost Optimization**: Right-sizing and cost monitoring
- **Backup & Recovery**: Proper backup strategies

### Development Standards:
- **Code Over Documentation**: Trust working code, verify with tests
- **Never Rush**: Quality over speed, even under pressure
- **Test Everything**: Unit, integration, and end-to-end tests
- **Version Control**: Meaningful commits and branching strategy
- **Error Handling**: Graceful degradation and proper logging

## 🔍 Code-First Approach

### Always Verify Through Code:
- **Read the actual implementation** - don't assume from docs
- **Test the real behavior** - don't trust documentation claims
- **Validate with working examples** - run code to confirm
- **Check source code** when documentation is unclear
- **Write tests** to document expected behavior

### Never Rush Implementation:
- **Take time to understand** the problem fully
- **Research proper solutions** before coding
- **Follow AWS Well-Architected** principles always
- **Review code thoroughly** before deployment
- **Test comprehensively** before marking complete

---

**Remember: Better to have a partially working real system than a fully working fake one.**
