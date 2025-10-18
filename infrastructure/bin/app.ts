#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AgentCoreStack } from '../lib/agentcore-stack';
import { SecurityStack } from '../lib/security-stack';
import { MonitoringStack } from '../lib/monitoring-stack';
import { FrontendStack } from '../lib/frontend-stack';

const app = new cdk.App();

// Get environment from context - ALWAYS use us-east-1
const environment = app.node.tryGetContext('environment') || 'development';
const region = 'us-east-1'; // Fixed region for consistency
const account = app.node.tryGetContext('account') || process.env.CDK_DEFAULT_ACCOUNT;

// Environment-specific configuration
const config = {
  development: {
    memoryRetentionDays: 7,
    enableDetailedMonitoring: false,
    logLevel: 'DEBUG',
    destroyOnRemoval: true
  },
  staging: {
    memoryRetentionDays: 14,
    enableDetailedMonitoring: true,
    logLevel: 'INFO',
    destroyOnRemoval: false
  },
  production: {
    memoryRetentionDays: 30,
    enableDetailedMonitoring: true,
    logLevel: 'INFO',
    destroyOnRemoval: false
  }
};

const envConfig = config[environment as keyof typeof config] || config.development;

// Consistent naming for cross-account deployment
const stackPrefix = `SecurityChatbot-${environment}`;

// Security Stack - IAM roles, Cognito, security groups
const securityStack = new SecurityStack(app, `${stackPrefix}-Security`, {
  env: { account, region },
  environment,
  stackName: `${stackPrefix}-Security`,
  ...envConfig
});

// AgentCore Stack - Memory, Gateway, Runtime
const agentCoreStack = new AgentCoreStack(app, `${stackPrefix}-AgentCore`, {
  env: { account, region },
  environment,
  stackName: `${stackPrefix}-AgentCore`,
  cognitoUserPool: securityStack.cognitoUserPool,
  agentRole: securityStack.agentRole,
  gatewayRole: securityStack.gatewayRole,
  runtimeRole: securityStack.runtimeRole,
  ...envConfig
});

// Frontend Stack - React app hosting
const frontendStack = new FrontendStack(app, `${stackPrefix}-Frontend`, {
  env: { account, region },
  environment,
  stackName: `${stackPrefix}-Frontend`
});

// Monitoring Stack - CloudWatch, alarms, dashboards
const monitoringStack = new MonitoringStack(app, `${stackPrefix}-Monitoring`, {
  env: { account, region },
  environment,
  stackName: `${stackPrefix}-Monitoring`,
  agentCoreResources: {
    memoryId: agentCoreStack.memoryId,
    gatewayUrl: agentCoreStack.gatewayUrl,
    runtimeArn: agentCoreStack.runtimeArn
  },
  ...envConfig
});

// Add dependencies
agentCoreStack.addDependency(securityStack);
monitoringStack.addDependency(agentCoreStack);

// Consistent tagging for all resources
cdk.Tags.of(app).add('Project', 'aws-security-agentcore-chatbot');
cdk.Tags.of(app).add('Environment', environment);
cdk.Tags.of(app).add('Region', region);
cdk.Tags.of(app).add('Owner', 'security-team');
cdk.Tags.of(app).add('CostCenter', 'security-operations');
cdk.Tags.of(app).add('ManagedBy', 'CDK');
cdk.Tags.of(app).add('Repository', 'aws-security-agentcore-chatbot');
