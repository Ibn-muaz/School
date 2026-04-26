#!/usr/bin/env python3
"""
Test script to verify Sanga Portal API endpoints
Run this after starting the Django server to test basic functionality
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:8000/api'

def test_endpoint(url, method='GET', data=None, headers=None):
    """Test an API endpoint"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"Unsupported method: {method}")
            return False

        print(f"{method} {url} - Status: {response.status_code}")
        if response.status_code >= 200 and response.status_code < 300:
            print("✓ Success")
            return True
        else:
            print(f"✗ Failed: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Error connecting to {url}: {e}")
        return False

def main():
    """Run basic API tests"""
    print("Testing Sanga Portal API endpoints...")
    print("=" * 50)

    # Test authentication endpoints (should return 400 for missing data, but server should respond)
    print("\n1. Testing Authentication Endpoints:")
    test_endpoint(f"{BASE_URL}/auth/login/", 'POST', {"username": "", "password": ""})

    # Test if Django server is running
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✓ Django server is running (root URL accessible)")
        else:
            print(f"✗ Django server root URL returned status {response.status_code}")
    except requests.exceptions.RequestException:
        print("✗ Cannot connect to Django server. Make sure it's running with 'python manage.py runserver'")
        sys.exit(1)

    # Test frontend server
    try:
        response = requests.get("http://localhost:3000/")
        if response.status_code == 200:
            print("✓ Frontend server is running")
        else:
            print(f"✗ Frontend server returned status {response.status_code}")
    except requests.exceptions.RequestException:
        print("✗ Cannot connect to frontend server. Make sure it's running with 'python server.py'")

    print("\n" + "=" * 50)
    print("Basic connectivity test completed.")
    print("For full API testing, create test users and use proper authentication tokens.")

if __name__ == "__main__":
    main()