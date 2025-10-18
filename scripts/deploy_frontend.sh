#!/bin/bash
set -e

echo "🚀 Deploying Frontend to AWS..."

# Build React app
cd src/frontend
echo "📦 Installing dependencies..."
npm install

echo "🔨 Building React app..."
npm run build

cd ../..

# Deploy with CDK
echo "☁️ Deploying to AWS..."
npx cdk deploy SecurityChatbot-development-Frontend --require-approval never

echo "✅ Frontend deployed successfully!"
