#!/usr/bin/env python3
"""
Complete UI Chatbot Test
Tests the full end-to-end functionality of the AWS Security Chatbot
"""

import requests
import json
import time

def test_api_gateway():
    """Test the API Gateway endpoint directly"""
    print("🧪 Testing API Gateway endpoint...")
    
    url = "https://hinh3actqf.execute-api.us-east-1.amazonaws.com/prod/chat"
    payload = {
        "message": "What is my security status?",
        "sessionId": f"test-session-{int(time.time())}"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Gateway Response: {data.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ API Gateway Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API Gateway Exception: {e}")
        return False

def test_website_accessibility():
    """Test if the website is accessible"""
    print("\n🌐 Testing website accessibility...")
    
    url = "http://aws-security-chatbot-ui-2024.s3-website-us-east-1.amazonaws.com"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200 and "AWS Security Chatbot" in response.text:
            print("✅ Website is accessible and contains expected content")
            return True
        else:
            print(f"❌ Website Error: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Website Exception: {e}")
        return False

def test_cors_headers():
    """Test CORS headers on API Gateway"""
    print("\n🔒 Testing CORS configuration...")
    
    url = "https://hinh3actqf.execute-api.us-east-1.amazonaws.com/prod/chat"
    
    try:
        # Test OPTIONS request
        response = requests.options(url, headers={
            'Origin': 'http://aws-security-chatbot-ui-2024.s3-website-us-east-1.amazonaws.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        })
        
        print(f"OPTIONS Status Code: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        
        if 'access-control-allow-origin' in response.headers:
            print("✅ CORS headers are present")
            return True
        else:
            print("❌ CORS headers missing")
            return False
            
    except Exception as e:
        print(f"❌ CORS Test Exception: {e}")
        return False

def main():
    """Run all tests"""
    print("🛡️ AWS Security Chatbot - Complete UI Test")
    print("=" * 50)
    
    results = []
    
    # Test 1: Website Accessibility
    results.append(test_website_accessibility())
    
    # Test 2: API Gateway
    results.append(test_api_gateway())
    
    # Test 3: CORS Configuration
    results.append(test_cors_headers())
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The UI chatbot is fully functional!")
        print(f"\n🌐 Access your chatbot at:")
        print(f"   http://aws-security-chatbot-ui-2024.s3-website-us-east-1.amazonaws.com")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main()
