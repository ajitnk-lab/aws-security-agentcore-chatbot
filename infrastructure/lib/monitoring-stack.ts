import * as cdk from 'aws-cdk-lib';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import { Construct } from 'constructs';

export interface MonitoringStackProps extends cdk.StackProps {
  environment: string;
  agentCoreResources: {
    memoryId: string;
    gatewayUrl: string;
    runtimeArn: string;
  };
  enableDetailedMonitoring?: boolean;
}

export class MonitoringStack extends cdk.Stack {
  public readonly dashboard: cloudwatch.Dashboard;

  constructor(scope: Construct, id: string, props: MonitoringStackProps) {
    super(scope, id, props);

    // Create CloudWatch Dashboard
    this.dashboard = new cloudwatch.Dashboard(this, 'SecurityChatbotDashboard', {
      dashboardName: `security-chatbot-${props.environment}`,
    });

    // Add basic widgets (will be enhanced with actual metrics)
    this.dashboard.addWidgets(
      new cloudwatch.TextWidget({
        markdown: `# AWS Security AgentCore Chatbot - ${props.environment.toUpperCase()}
        
## System Overview
- Memory: ${props.agentCoreResources.memoryId}
- Gateway: ${props.agentCoreResources.gatewayUrl}  
- Runtime: ${props.agentCoreResources.runtimeArn}

## Status
Dashboard initialized - metrics will be added as resources are deployed.

## Architecture
\`\`\`
Chat UI ↔ Bedrock Agent ↔ AgentCore Gateway ↔ AgentCore Runtime ↔ MCP Server ↔ AWS Security Services
\`\`\``,
        width: 24,
        height: 8,
      })
    );

    // Output dashboard URL
    new cdk.CfnOutput(this, 'DashboardUrl', {
      value: `https://console.aws.amazon.com/cloudwatch/home?region=${this.region}#dashboards:name=${this.dashboard.dashboardName}`,
      description: 'CloudWatch Dashboard URL',
    });
  }
}
