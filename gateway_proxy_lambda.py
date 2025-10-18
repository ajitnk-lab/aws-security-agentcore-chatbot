import json
import requests
import boto3

def lambda_handler(event, context):
    """
    Proxy Lambda: Bedrock Agent -> Gateway
    """
    
    # Gateway URL
    gateway_url = "https://security-runtime-gateway-dtga85g9fh.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
    
    # Get Cognito token for Gateway auth
    cognito = boto3.client('cognito-idp', region_name='us-east-1')
    
    try:
        # Get OAuth token
        auth_response = cognito.initiate_auth(
            ClientId='31tulnklmj2kcslkmgcbme7n9v',
            AuthFlow='CLIENT_CREDENTIALS'
        )
        token = auth_response['AuthenticationResult']['AccessToken']
        
        # Extract tool call from Bedrock Agent event
        operation_id = event.get('actionGroup', '')
        parameters = event.get('parameters', [])
        
        # Map to MCP call
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list" if operation_id == "list_tools" else "tools/call",
            "params": {}
        }
        
        # Call Gateway
        response = requests.post(
            gateway_url,
            json=mcp_request,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'actionGroup': event.get('actionGroup', ''),
                'apiPath': event.get('apiPath', ''),
                'httpMethod': event.get('httpMethod', ''),
                'httpStatusCode': 200,
                'responseBody': {
                    'application/json': {
                        'body': json.dumps(result.get('result', {}))
                    }
                }
            }
        else:
            return {
                'actionGroup': event.get('actionGroup', ''),
                'apiPath': event.get('apiPath', ''),
                'httpMethod': event.get('httpMethod', ''),
                'httpStatusCode': 500,
                'responseBody': {
                    'application/json': {
                        'body': json.dumps({'error': f'Gateway error: {response.status_code}'})
                    }
                }
            }
            
    except Exception as e:
        return {
            'actionGroup': event.get('actionGroup', ''),
            'apiPath': event.get('apiPath', ''),
            'httpMethod': event.get('httpMethod', ''),
            'httpStatusCode': 500,
            'responseBody': {
                'application/json': {
                    'body': json.dumps({'error': str(e)})
                }
            }
        }
