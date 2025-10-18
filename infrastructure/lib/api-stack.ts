import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export interface ApiStackProps extends cdk.StackProps {
  environment: string;
}

export class ApiStack extends cdk.Stack {
  public readonly apiUrl: string;

  constructor(scope: Construct, id: string, props: ApiStackProps) {
    super(scope, id, props);

    // Lambda function for chat API
    const chatFunction = new lambda.Function(this, 'ChatFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
const { BedrockAgentRuntimeClient, InvokeAgentCommand } = require('@aws-sdk/client-bedrock-agent-runtime');

const client = new BedrockAgentRuntimeClient({ region: 'us-east-1' });

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers };
  }

  try {
    const { message, sessionId } = JSON.parse(event.body);
    
    const command = new InvokeAgentCommand({
      agentId: 'VS4IAMTUZO',
      agentAliasId: 'OUUY9MTH8E',
      sessionId: sessionId || \`session-\${Date.now()}\`,
      inputText: message
    });

    const response = await client.send(command);
    
    let assistantResponse = '';
    for await (const eventItem of response.completion) {
      if (eventItem.chunk?.bytes) {
        assistantResponse += new TextDecoder().decode(eventItem.chunk.bytes);
      }
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ response: assistantResponse })
    };
  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
      `),
      timeout: cdk.Duration.seconds(30)
    });

    // Add Bedrock permissions
    chatFunction.addToRolePolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'bedrock-agent-runtime:InvokeAgent'
      ],
      resources: ['*']
    }));

    // API Gateway
    const api = new apigateway.RestApi(this, 'ChatApi', {
      restApiName: `security-chatbot-api-${props.environment}`,
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: ['Content-Type', 'Authorization']
      }
    });

    const chatResource = api.root.addResource('chat');
    chatResource.addMethod('POST', new apigateway.LambdaIntegration(chatFunction));

    this.apiUrl = api.url;

    new cdk.CfnOutput(this, 'ApiUrl', {
      value: this.apiUrl,
      description: 'Chat API URL'
    });
  }
}
