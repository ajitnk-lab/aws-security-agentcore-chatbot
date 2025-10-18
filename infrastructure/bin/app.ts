#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AgentCoreStack } from '../lib/agentcore-stack';
import { SecurityStack } from '../lib/security-stack';
import { MonitoringStack } from '../lib/monitoring-stack';

const app = new cdk.App();

// Get environment from context
const environment = app.node.tryGetContext('environment') || 'development';
const region = app.node.tryGetContext('region') || 'us-west-2';

// Environment-specific configuration
const config = {
  development: {
    memoryRetentionDays: 7,
    enableDetailedMonitoring: false,
    logLevel: 'DEBUG'
  },
  production: {
    memoryRetentionDays: 30,
    enableDetailedMonitoring: true,
    logLevel: 'INFO'
  }
};

const envConfig = config[environment as keyof typeof config] || config.development;

// Security Stack - IAM roles, Cognito, security groups
const securityStack = new SecurityStack(app, `SecurityStack-${environment}`, {
  env: { region },
  environment,
  ...envConfig
});

// AgentCore Stack - Memory, Gateway, Runtime
const agentCoreStack = new AgentCoreStack(app, `AgentCoreStack-${environment}`, {
  env: { region },
  environment,
  cognitoUserPool: securityStack.cognitoUserPool,
  agentRole: securityStack.agentRole,
  gatewayRole: securityStack.gatewayRole,
  runtimeRole: securityStack.runtimeRole,
  ...envConfig
});

// Monitoring Stack - CloudWatch, alarms, dashboards
const monitoringStack = new MonitoringStack(app, `MonitoringStack-${environment}`, {
  env: { region },
  environment,
  agentCoreResources: {
    memory: agentCoreStack.memory,
    gateway: agentCoreStack.gateway,
    runtime: agentCoreStack.runtime
  },
  ...envConfig
});

// Add dependencies
agentCoreStack.addDependency(securityStack);
monitoringStack.addDependency(agentCoreStack);

// Add tags
cdk.Tags.of(app).add('Project', 'aws-security-agentcore-chatbot');
cdk.Tags.of(app).add('Environment', environment);
cdk.Tags.of(app).add('Owner', 'security-team');
cdk.Tags.of(app).add('CostCenter', 'security-operations');
