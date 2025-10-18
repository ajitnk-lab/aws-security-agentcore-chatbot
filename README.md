# AWS Security AgentCore Chatbot 🛡️🤖

An intelligent AWS security chatbot built with Amazon Bedrock AgentCore that provides real-time security insights, compliance checking, and recommendations through natural language conversations.

## 🎯 Overview

This solution deploys a production-ready security assistant that leverages:
- **AWS Well-Architected Security MCP Server** for security analysis tools
- **Amazon Bedrock AgentCore** for intelligent conversation and memory
- **Claude 3.7 Sonnet** for natural language understanding
- **Infrastructure as Code** with AWS CDK for reliable deployments

## 🏗️ Architecture

```
Chat UI ↔ Bedrock Agent ↔ AgentCore Gateway ↔ MCP Server ↔ AWS Security Services
           ↕                    ↕
    AgentCore Memory    AgentCore Runtime
```

## 🚀 Quick Start

### Prerequisites
- AWS Account with appropriate permissions
- AWS CLI configured (`aws configure`)
- Node.js 18+ and Python 3.10+
- Git and GitHub access

### Installation
```bash
# Clone repository
git clone https://github.com/ajitnk-lab/aws-security-agentcore-chatbot.git
cd aws-security-agentcore-chatbot

# Install dependencies
npm install
pip install -r requirements.txt

# Deploy infrastructure
npm run deploy
```

## 🛠️ Features

### Security Capabilities
- ✅ **Security Service Status**: Check GuardDuty, Security Hub, Inspector status
- ✅ **Security Findings**: Retrieve and analyze findings from multiple services
- ✅ **Compliance Checking**: Validate storage encryption and network security
- ✅ **Service Discovery**: List AWS services in use across regions
- ✅ **Intelligent Recommendations**: AI-powered security guidance

### Conversation Features
- 🧠 **Persistent Memory**: Remembers context across sessions
- 🔍 **Semantic Search**: Finds relevant past security information
- 💬 **Natural Language**: Ask questions in plain English
- 📊 **Visual Reports**: Security findings with charts and graphs

## 💬 Example Conversations

```
User: "What's my security status?"
Bot: "I'll check your security services... GuardDuty and Security Hub are enabled. 
     Let me look for any findings... No critical issues found. Your security 
     posture looks good!"

User: "Are my S3 buckets encrypted?"
Bot: "Checking storage encryption... Found 15 S3 buckets, 14 are encrypted with 
     AES-256. One bucket 'legacy-data-bucket' needs encryption enabled."

User: "Show me network security issues"
Bot: "Analyzing network security... Found 2 load balancers without HTTPS 
     listeners and 1 security group with overly permissive rules."
```

## 📁 Project Structure

```
├── docs/                   # Documentation
│   ├── requirements.md     # Detailed requirements
│   ├── design.md          # System design
│   └── task.md            # Implementation tasks
├── infrastructure/         # CDK infrastructure code
│   ├── lib/               # CDK constructs
│   └── bin/               # CDK app entry point
├── src/                   # Application source code
│   ├── mcp-server/        # MCP server implementation
│   ├── agent/             # Bedrock agent configuration
│   └── frontend/          # Chat interface
├── tests/                 # Test suites
└── scripts/               # Deployment and utility scripts
```

## 🔧 Development

### Local Testing
```bash
# Test MCP server locally
cd src/mcp-server
python test_tools.py

# Test agent integration
agentcore invoke '{"prompt": "What is my security status?"}'

# Run frontend locally
cd src/frontend
npm run dev
```

### Deployment
```bash
# Deploy to development
npm run deploy:dev

# Deploy to production
npm run deploy:prod
```

## 📊 Monitoring

Access monitoring dashboards:
- **System Health**: CloudWatch dashboard for infrastructure metrics
- **Agent Performance**: Response times and success rates
- **Security Metrics**: Security findings and compliance trends
- **Cost Tracking**: Resource usage and cost optimization

## 🛡️ Security

- **Authentication**: OAuth2 with Amazon Cognito
- **Authorization**: IAM roles with least-privilege access
- **Encryption**: Data encrypted at rest and in transit
- **Audit Logging**: Complete audit trail of all interactions

## 📚 Documentation

- [Requirements](docs/requirements.md) - Detailed project requirements
- [System Design](docs/design.md) - Architecture and component details
- [Implementation Tasks](docs/task.md) - Development roadmap
- [API Documentation](docs/api.md) - MCP server API reference
- [Deployment Guide](docs/deployment.md) - Step-by-step deployment
- [User Guide](docs/user-guide.md) - How to use the chatbot

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/ajitnk-lab/aws-security-agentcore-chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ajitnk-lab/aws-security-agentcore-chatbot/discussions)
- **Documentation**: [Project Wiki](https://github.com/ajitnk-lab/aws-security-agentcore-chatbot/wiki)

## 🏆 Acknowledgments

- AWS Well-Architected Security Pillar team
- Amazon Bedrock AgentCore team
- Model Context Protocol (MCP) community
- AWS CDK community

---

**Built with ❤️ for AWS Security**
