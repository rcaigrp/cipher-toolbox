#!/usr/bin/env python3
"""
Check for authentication bypass vulnerabilities in exposed APIs.
This script tests basic access control on common endpoints.
"""

import requests
import sys
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:8000"  # Example URL, change as needed
TEST_ENDPOINTS = [
    "/api/admin",
    "/api/users",
    "/api/settings",
    "/api/config"
]

def check_endpoint(url):
    """Check if an endpoint is accessible without authentication."""
    try:
        response = requests.get(url, timeout=5)
        # If it returns 200 or 403, it's probably not protected
        # If it returns 401, authentication is required
        return response.status_code
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return None

def main():
    exposed_endpoints = []
    
    for endpoint in TEST_ENDPOINTS:
        full_url = urljoin(BASE_URL, endpoint)
        status = check_endpoint(full_url)
        
        if status is not None:
            print(f"{full_url}: Status Code {status}")
            if status in [200, 403]:
                exposed_endpoints.append(full_url)
    
    if exposed_endpoints:
        print("\nPotentially exposed endpoints:")
        for endpoint in exposed_endpoints:
            print(f"  - {endpoint}")
        return 1
    else:
        print("No obvious authentication bypasses detected.")
        return 0

if __name__ == "__main__":
    sys.exit(main())