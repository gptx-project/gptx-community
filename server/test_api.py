"""
Test script for the Bettercorp Contributor Portal API.

This script tests the basic functionality of the API endpoints.
"""

import requests
import json
from typing import Dict, Any, Optional

# API base URL
BASE_URL = "http://localhost:8000/api"

# Test user credentials
TEST_USER = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword",
    "full_name": "Test User",
}

# Access token
access_token = None

def print_response(response: requests.Response) -> None:
    """
    Print the response details.
    
    Args:
        response: Response object
    """
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("-" * 80)

def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None,
) -> requests.Response:
    """
    Make a request to the API.
    
    Args:
        method: HTTP method
        endpoint: API endpoint
        data: Request data
        token: Access token
        
    Returns:
        Response: Response object
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if method.upper() == "GET":
        response = requests.get(url, headers=headers)
    elif method.upper() == "POST":
        headers["Content-Type"] = "application/json"
        response = requests.post(url, json=data, headers=headers)
    elif method.upper() == "PUT":
        headers["Content-Type"] = "application/json"
        response = requests.put(url, json=data, headers=headers)
    elif method.upper() == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return response

def test_health_check() -> None:
    """Test the health check endpoint."""
    print("\n=== Testing Health Check ===")
    response = requests.get("http://localhost:8000/health")
    print_response(response)

def test_register_user() -> None:
    """Test user registration."""
    print("\n=== Testing User Registration ===")
    response = make_request("POST", "/auth/register", TEST_USER)
    print_response(response)

def test_login() -> None:
    """Test user login."""
    global access_token
    
    print("\n=== Testing User Login ===")
    login_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
    }
    
    # Use form data for token endpoint
    response = requests.post(
        f"{BASE_URL}/auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    print_response(response)
    
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print(f"Access Token: {access_token}")

def test_get_current_user() -> None:
    """Test getting current user information."""
    print("\n=== Testing Get Current User ===")
    response = make_request("GET", "/users/me", token=access_token)
    print_response(response)

def test_create_project() -> None:
    """Test creating a project."""
    print("\n=== Testing Create Project ===")
    project_data = {
        "name": "Test Project",
        "description": "A test project",
    }
    response = make_request("POST", "/projects", project_data, access_token)
    print_response(response)

def main() -> None:
    """Run the tests."""
    try:
        # Test health check
        test_health_check()
        
        # Test user registration and login
        test_register_user()
        test_login()
        
        if access_token:
            # Test authenticated endpoints
            test_get_current_user()
            test_create_project()
        else:
            print("Skipping authenticated tests because login failed.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()