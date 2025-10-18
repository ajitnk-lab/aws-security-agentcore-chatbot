import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import { Construct } from 'constructs';

export interface SecurityStackProps extends cdk.StackProps {
  environment: string;
  destroyOnRemoval?: boolean;
}

export class SecurityStack extends cdk.Stack {
  public readonly cognitoUserPool: cognito.UserPool;
  public readonly agentRole: iam.Role;
  public readonly gatewayRole: iam.Role;
  public readonly runtimeRole: iam.Role;

  constructor(scope: Construct, id: string, props: SecurityStackProps) {
    super(scope, id, props);

    // Cognito User Pool for authentication
    this.cognitoUserPool = new cognito.UserPool(this, 'SecurityChatbotUserPool', {
      userPoolName: `security-chatbot-${props.environment}`,
      selfSignUpEnabled: true,
      signInAliases: {
        email: true,
      },
      autoVerify: {
        email: true,
      },
      removalPolicy: props.destroyOnRemoval ? cdk.RemovalPolicy.DESTROY : cdk.RemovalPolicy.RETAIN,
    });

    // IAM Role for Bedrock Agent
    this.agentRole = new iam.Role(this, 'AgentRole', {
      assumedBy: new iam.ServicePrincipal('bedrock.amazonaws.com'),
      description: 'Role for Bedrock Agent to access AgentCore services',
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonBedrockFullAccess'),
      ],
    });

    // IAM Role for AgentCore Gateway
    this.gatewayRole = new iam.Role(this, 'GatewayRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      description: 'Role for AgentCore Gateway',
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ],
    });

    // IAM Role for AgentCore Runtime
    this.runtimeRole = new iam.Role(this, 'RuntimeRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      description: 'Role for AgentCore Runtime MCP server',
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ],
    });

    // Add security service permissions to runtime role
    this.runtimeRole.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'guardduty:GetDetector',
        'guardduty:ListDetectors',
        'guardduty:GetFindings',
        'securityhub:GetFindings',
        'securityhub:DescribeHub',
        'inspector2:ListFindings',
        'inspector2:GetFindings',
        'trustedadvisor:Describe*',
        'support:*',
        'iam:GetAccountSummary',
        'iam:ListAccessAnalyzers',
        'access-analyzer:ListFindings',
        'macie2:GetFindings',
        'macie2:DescribeOrganizationConfiguration',
      ],
      resources: ['*'],
    }));
  }
}
