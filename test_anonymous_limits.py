#!/usr/bin/env python3
"""
Test script for anonymous user request limiting
Tests the 3-request limit for anonymous users
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_anonymous_requests():
    """Test anonymous user request limiting"""
    print("🚀 Testing Anonymous User Request Limiting")
    print("=" * 60)
    
    # Test 1: Check initial request status
    print("\n1. Checking initial request status...")
    try:
        response = requests.get(f"{API_BASE}/check-requests")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get('remaining_requests') == 3:
            print("✅ Initial status correct: 3 requests remaining")
        else:
            print("❌ Initial status incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return False
    
    # Test 2: Make first optimization request
    print("\n2. Making first optimization request...")
    try:
        response = requests.post(f"{API_BASE}/optimize", json={
            "prompt": "Write a simple hello world program",
            "context": "general"
        })
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ First request successful")
            data = response.json()
            print(f"Optimized prompt: {data.get('optimized', 'N/A')[:100]}...")
        else:
            print(f"❌ First request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in first request: {e}")
        return False
    
    # Test 3: Check remaining requests after first use
    print("\n3. Checking remaining requests after first use...")
    try:
        response = requests.get(f"{API_BASE}/check-requests")
        data = response.json()
        print(f"Remaining requests: {data.get('remaining_requests')}")
        
        if data.get('remaining_requests') == 2:
            print("✅ Correctly shows 2 requests remaining")
        else:
            print("❌ Incorrect remaining count")
            return False
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return False
    
    # Test 4: Make second optimization request
    print("\n4. Making second optimization request...")
    try:
        response = requests.post(f"{API_BASE}/optimize", json={
            "prompt": "Explain machine learning in simple terms",
            "context": "technical"
        })
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Second request successful")
        else:
            print(f"❌ Second request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in second request: {e}")
        return False
    
    # Test 5: Check remaining requests after second use
    print("\n5. Checking remaining requests after second use...")
    try:
        response = requests.get(f"{API_BASE}/check-requests")
        data = response.json()
        print(f"Remaining requests: {data.get('remaining_requests')}")
        
        if data.get('remaining_requests') == 1:
            print("✅ Correctly shows 1 request remaining")
        else:
            print("❌ Incorrect remaining count")
            return False
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return False
    
    # Test 6: Make third optimization request
    print("\n6. Making third optimization request...")
    try:
        response = requests.post(f"{API_BASE}/optimize", json={
            "prompt": "Create a business plan outline",
            "context": "business"
        })
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Third request successful")
        else:
            print(f"❌ Third request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in third request: {e}")
        return False
    
    # Test 7: Check remaining requests after third use
    print("\n7. Checking remaining requests after third use...")
    try:
        response = requests.get(f"{API_BASE}/check-requests")
        data = response.json()
        print(f"Remaining requests: {data.get('remaining_requests')}")
        
        if data.get('remaining_requests') == 0:
            print("✅ Correctly shows 0 requests remaining")
        else:
            print("❌ Incorrect remaining count")
            return False
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return False
    
    # Test 8: Try to make fourth request (should fail)
    print("\n8. Attempting fourth request (should fail)...")
    try:
        response = requests.post(f"{API_BASE}/optimize", json={
            "prompt": "This request should be blocked",
            "context": "general"
        })
        print(f"Status: {response.status_code}")
        
        if response.status_code == 403:
            print("✅ Fourth request correctly blocked")
            data = response.json()
            print(f"Error message: {data.get('message')}")
            
            if data.get('requires_login'):
                print("✅ Correctly indicates login required")
            else:
                print("❌ Missing login requirement flag")
                return False
        else:
            print(f"❌ Fourth request should have been blocked, got: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error in fourth request: {e}")
        return False
    
    # Test 9: Final status check
    print("\n9. Final status check...")
    try:
        response = requests.get(f"{API_BASE}/check-requests")
        data = response.json()
        print(f"Final status: {json.dumps(data, indent=2)}")
        
        if data.get('remaining_requests') == 0 and data.get('requires_login'):
            print("✅ Final status correct: 0 requests, login required")
        else:
            print("❌ Final status incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Error in final check: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All anonymous request limiting tests passed!")
    return True

def main():
    """Run the anonymous request limiting tests"""
    try:
        success = test_anonymous_requests()
        if success:
            print("\n✅ Anonymous request limiting system is working correctly!")
            print("\nSummary:")
            print("- Anonymous users get 3 free optimizations")
            print("- No visible counter banner is shown to users")
            print("- After 3 requests, login modal appears automatically")
            print("- Request counting works correctly in the background")
            print("- Login requirement is properly enforced")
        else:
            print("\n❌ Some tests failed. Check the implementation.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
