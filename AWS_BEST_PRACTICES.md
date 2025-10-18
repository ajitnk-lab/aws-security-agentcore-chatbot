# 🏆 AWS Best Practices - Non-Negotiable Standards

## 🛡️ Security First

### IAM & Access Management
```typescript
// ✅ CORRECT - Least privilege IAM role
const mcpServerRole = new iam.Role(this, 'MCPServerRole', {
  assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
  managedPolicies: [
    iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')
  ],
  inlinePolicies: {
    SecurityServicesRead: new iam.PolicyDocument({
      statements: [
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: [
            'guardduty:GetDetector',
            'securityhub:DescribeHub'
          ],
          resources: ['*']
        })
      ]
    })
  }
});

// ❌ WRONG - Overly broad permissions
// Don't use: 'guardduty:*' or '*:*'
```

### Encryption & Secrets
```typescript
// ✅ CORRECT - Encrypted storage
const memory = new Memory(this, 'SecurityMemory', {
  encryption: MemoryEncryption.AWS_MANAGED,
  retentionPeriod: Duration.days(30)
});

// ✅ CORRECT - Secrets management
const apiKey = secretsmanager.Secret.fromSecretNameV2(this, 'APIKey', 'agentcore/api-key');

// ❌ WRONG - Hardcoded secrets
// const apiKey = 'sk-1234567890abcdef'; // NEVER DO THIS
```

## 🏗️ Infrastructure as Code

### CDK Best Practices
```typescript
// ✅ CORRECT - Proper resource naming and tagging
export class AgentCoreStack extends Stack {
  constructor(scope: Construct, id: string, props: AgentCoreStackProps) {
    super(scope, id, props);
    
    // Consistent naming convention
    const resourcePrefix = `security-chatbot-${props.environment}`;
    
    // Proper tagging
    Tags.of(this).add('Project', 'aws-security-agentcore-chatbot');
    Tags.of(this).add('Environment', props.environment);
    Tags.of(this).add('Owner', 'security-team');
    Tags.of(this).add('CostCenter', 'security-operations');
  }
}

// ✅ CORRECT - Environment-specific configuration
const config = {
  development: {
    memoryRetentionDays: 7,
    logLevel: 'DEBUG'
  },
  production: {
    memoryRetentionDays: 30,
    logLevel: 'INFO'
  }
};
```

## 📊 Monitoring & Observability

### CloudWatch Integration
```typescript
// ✅ CORRECT - Comprehensive monitoring
const dashboard = new cloudwatch.Dashboard(this, 'SecurityChatbotDashboard', {
  dashboardName: `security-chatbot-${props.environment}`,
  widgets: [
    [
      new cloudwatch.GraphWidget({
        title: 'Agent Response Times',
        left: [agentResponseTimeMetric],
        width: 12
      })
    ],
    [
      new cloudwatch.GraphWidget({
        title: 'MCP Tool Execution',
        left: [mcpToolSuccessMetric, mcpToolErrorMetric],
        width: 12
      })
    ]
  ]
});

// ✅ CORRECT - Proper alarms
new cloudwatch.Alarm(this, 'HighErrorRate', {
  metric: errorRateMetric,
  threshold: 5, // 5% error rate
  evaluationPeriods: 2,
  alarmDescription: 'High error rate in security chatbot'
});
```

## 🔍 Code-First Approach

### Verification Through Code
```python
# ✅ CORRECT - Test actual behavior
def test_mcp_server_integration():
    """Test real MCP server with actual AWS calls"""
    client = MCPClient(server_url=REAL_SERVER_URL)
    
    # Test with real AWS credentials
    response = client.call_tool('CheckSecurityServices', {
        'region': 'us-east-1',
        'services': ['guardduty']
    })
    
    # Verify real AWS data structure
    assert 'service_statuses' in response
    assert 'guardduty' in response['service_statuses']
    assert response['service_statuses']['guardduty']['enabled'] in [True, False]

# ❌ WRONG - Mock testing only
# def test_fake_response():
#     return {"status": "success", "fake": True}
```

### Documentation vs Code
```python
# ✅ CORRECT - Trust code, verify behavior
def verify_agentcore_memory():
    """Verify memory behavior through actual usage"""
    memory_client = MemoryClient(region_name='us-west-2')
    
    # Create and test real memory resource
    memory = memory_client.create_memory_and_wait(
        name="test-memory",
        strategies=[]
    )
    
    # Verify actual behavior
    session = memory_client.create_session(
        memory_id=memory['id'],
        actor_id='test-user'
    )
    
    # Test real operations
    session.add_turns([
        ConversationalMessage("Test message", MessageRole.USER)
    ])
    
    turns = session.get_last_k_turns(k=1)
    assert len(turns) == 1
    
    # Clean up
    memory_client.delete_memory(memory_id=memory['id'])
```

## ⚡ Never Rush - Quality Standards

### Proper Error Handling
```python
# ✅ CORRECT - Comprehensive error handling
async def call_security_service(service_name: str, region: str):
    try:
        if service_name == 'guardduty':
            client = boto3.client('guardduty', region_name=region)
            response = client.list_detectors()
            return process_guardduty_response(response)
        elif service_name == 'securityhub':
            client = boto3.client('securityhub', region_name=region)
            response = client.describe_hub()
            return process_securityhub_response(response)
        else:
            raise ValueError(f"Unsupported service: {service_name}")
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            logger.error(f"Access denied for {service_name} in {region}")
            return {"error": "insufficient_permissions", "service": service_name}
        elif error_code == 'ServiceNotEnabled':
            logger.info(f"{service_name} not enabled in {region}")
            return {"enabled": False, "service": service_name}
        else:
            logger.error(f"Unexpected error for {service_name}: {e}")
            raise
    except Exception as e:
        logger.error(f"Unexpected error calling {service_name}: {e}")
        raise

# ❌ WRONG - Rushed error handling
# def call_service():
#     try:
#         return some_call()
#     except:
#         return {"error": "something went wrong"}
```

### Thorough Testing
```python
# ✅ CORRECT - Comprehensive test coverage
class TestSecurityChatbot:
    def test_end_to_end_flow(self):
        """Test complete user query to AWS response flow"""
        # Test real components, not mocks
        pass
    
    def test_memory_persistence(self):
        """Test conversation memory across sessions"""
        pass
    
    def test_error_scenarios(self):
        """Test proper error handling"""
        pass
    
    def test_security_compliance(self):
        """Test IAM permissions and encryption"""
        pass

# Run tests before every deployment
# pytest tests/ --cov=src/ --cov-report=html
```

## 📋 Quality Gates

### Before Any Deployment:
1. **Code Review**: All code reviewed for AWS best practices
2. **Security Scan**: CDK nag and security linting
3. **Test Coverage**: >80% test coverage with real integrations
4. **Performance Test**: Response times within SLA
5. **Cost Analysis**: Resource costs within budget

### Before Marking Tasks Complete:
1. **Real Integration**: Verified with actual AWS services
2. **Error Handling**: Proper error scenarios tested
3. **Monitoring**: Metrics and alarms configured
4. **Documentation**: Code comments and README updated
5. **Security**: IAM permissions reviewed and minimal

## 🎯 Success Metrics

- **Security**: Zero hardcoded secrets, least privilege IAM
- **Reliability**: >99.9% uptime, proper error handling
- **Performance**: <5s response times, efficient resource usage
- **Cost**: Within budget, right-sized resources
- **Maintainability**: Clean code, comprehensive tests

**Remember: AWS best practices are not optional - they are the foundation of reliable, secure, and cost-effective solutions.**
