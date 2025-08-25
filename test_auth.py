#!/usr/bin/env python3
"""
Simple test script for the authentication system
Run this after starting the Flask backend to test the auth endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api/auth"

def test_signup():
    """Test user signup"""
    print("Testing user signup...")
    
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/signup", json=signup_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Signup successful!")
            return response.json().get('token')
        else:
            print("❌ Signup failed!")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json().get('token')
        else:
            print("❌ Login failed!")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_profile(token):
    """Test getting user profile"""
    if not token:
        print("❌ No token available for profile test")
        return
        
    print("\nTesting get profile...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/profile", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Profile retrieval successful!")
        else:
            print("❌ Profile retrieval failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_verify_token(token):
    """Test token verification"""
    if not token:
        print("❌ No token available for verification test")
        return
        
    print("\nTesting token verification...")
    
    verify_data = {"token": token}
    
    try:
        response = requests.post(f"{API_BASE}/verify-token", json=verify_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Token verification successful!")
        else:
            print("❌ Token verification failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_logout(token):
    """Test user logout"""
    if not token:
        print("❌ No token available for logout test")
        return
        
    print("\nTesting user logout...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{API_BASE}/logout", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Logout successful!")
        else:
            print("❌ Logout failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def main():
    """Run all authentication tests"""
    print("🚀 Starting Authentication System Tests")
    print("=" * 50)
    
    # Test signup
    token = test_signup()
    
    # Test login
    login_token = test_login()
    
    # Use the login token for subsequent tests
    if login_token:
        token = login_token
    
    # Test profile retrieval
    test_profile(token)
    
    # Test token verification
    test_verify_token(token)
    
    # Test logout
    test_logout(token)
    
    print("\n" + "=" * 50)
    print("🏁 Authentication tests completed!")
    
    if token:
        print(f"Token: {token[:20]}...")
    else:
        print("No valid token obtained")

if __name__ == "__main__":
    main()
