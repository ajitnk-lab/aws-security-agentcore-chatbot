import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import { Construct } from 'constructs';

export interface AgentCoreStackProps extends cdk.StackProps {
  environment: string;
  cognitoUserPool: cognito.UserPool;
  agentRole: iam.Role;
  gatewayRole: iam.Role;
  runtimeRole: iam.Role;
  memoryRetentionDays?: number;
  destroyOnRemoval?: boolean;
}

export class AgentCoreStack extends cdk.Stack {
  public readonly memoryId: string;
  public readonly gatewayUrl: string;
  public readonly runtimeArn: string;

  constructor(scope: Construct, id: string, props: AgentCoreStackProps) {
    super(scope, id, props);

    // NOTE: AgentCore resources are deployed via CLI, not CDK
    // This stack documents the architecture and provides configuration

    // AgentCore Memory - deployed via: agentcore memory create
    this.memoryId = `mem-${props.environment}-security-chatbot`;

    // AgentCore Runtime - deployed via: agentcore launch
    this.runtimeArn = `arn:aws:bedrock-agentcore:${this.region}:${this.account}:runtime/agentcore_mcp_server-${props.environment}`;

    // AgentCore Gateway - deployed via: agentcore gateway create-mcp-gateway
    this.gatewayUrl = `https://security-chatbot-gateway-${props.environment}.gateway.bedrock-agentcore.${this.region}.amazonaws.com/mcp`;

    // Configuration for deployment scripts
    const deploymentConfig = {
      memory: {
        name: `SecurityChatbot_Memory_${props.environment}`,
        strategies: [
          {
            userPreferenceMemoryStrategy: {
              name: 'user_preferences',
              namespaces: ['/user/preferences']
            }
          },
          {
            semanticMemoryStrategy: {
              name: 'security_context',
              namespaces: ['/security/context', '/security/findings']
            }
          }
        ],
        eventExpiryDays: props.memoryRetentionDays || 7
      },
      runtime: {
        name: `security-mcp-server-${props.environment}`,
        entrypoint: 'agent.py',
        requirements: 'requirements.txt'
      },
      gateway: {
        name: `security-chatbot-gateway-${props.environment}`,
        authorizerType: 'COGNITO_USER_POOLS',
        userPoolId: props.cognitoUserPool.userPoolId,
        enableSemanticSearch: true
      }
    };

    // Store configuration for deployment scripts
    new cdk.CfnOutput(this, 'DeploymentConfig', {
      value: JSON.stringify(deploymentConfig),
      description: 'Configuration for AgentCore CLI deployment'
    });

    // Output resource identifiers
    new cdk.CfnOutput(this, 'MemoryId', {
      value: this.memoryId,
      description: 'AgentCore Memory Resource ID'
    });

    new cdk.CfnOutput(this, 'GatewayUrl', {
      value: this.gatewayUrl,
      description: 'AgentCore Gateway MCP URL'
    });

    new cdk.CfnOutput(this, 'RuntimeArn', {
      value: this.runtimeArn,
      description: 'AgentCore Runtime ARN'
    });

    // Deployment instructions
    new cdk.CfnOutput(this, 'DeploymentInstructions', {
      value: 'Run scripts/deploy_agentcore.sh after CDK deployment',
      description: 'Next steps for AgentCore deployment'
    });
  }
}
