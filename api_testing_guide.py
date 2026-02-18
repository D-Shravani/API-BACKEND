"""
API Testing Guide - Complete Examples for All Endpoints
======================================================

This file demonstrates how to test all API endpoints with sample data.
Run this script to see all operations in action.

Usage:
    python api_testing_guide.py
"""

import requests
import json
from time import sleep

# Configuration
BASE_URL = "http://127.0.0.1:5000"
SEPARATOR = "=" * 70

# Color codes for better visibility (Windows compatible)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{SEPARATOR}")
    print(f"  {text}")
    print(SEPARATOR)

def print_request(method, url, data=None, headers=None):
    """Print request details"""
    print(f"\n📤 REQUEST: {method} {url}")
    if data:
        print(f"   Body: {json.dumps(data, indent=2)}")
    if headers and 'Authorization' in headers:
        print(f"   Auth: Bearer token included")

def print_response(response):
    """Print response details"""
    status_color = Colors.GREEN if 200 <= response.status_code < 300 else Colors.RED
    print(f"\n📥 RESPONSE: {status_color}Status {response.status_code}{Colors.END}")
    try:
        print(f"   {json.dumps(response.json(), indent=2)}")
    except:
        print(f"   {response.text}")

def wait_for_server():
    """Check if server is running"""
    print("🔍 Checking if API server is running...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ Server is running!\n")
            return True
    except:
        pass
    
    print("❌ Server is not running!")
    print("Please start the server with: python app.py")
    return False

# ============================================================================
# TEST SCENARIOS
# ============================================================================

def test_1_health_check():
    """Test 1: Health Check - Verify API is running"""
    print_header("TEST 1: Health Check")
    
    url = f"{BASE_URL}/health"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 200

def test_2_login_admin():
    """Test 2: Login as Admin - Get JWT token for admin operations"""
    print_header("TEST 2: Login as Admin")
    
    url = f"{BASE_URL}/login"
    data = {"email": "admin@example.com"}
    
    print_request("POST", url, data)
    
    response = requests.post(url, json=data)
    print_response(response)
    
    if response.status_code == 200:
        token = response.json()['data']['token']
        print(f"\n💾 Admin Token Saved for subsequent requests")
        return token
    return None

def test_3_login_regular_user():
    """Test 3: Login as Regular User - Get JWT token for regular user"""
    print_header("TEST 3: Login as Regular User")
    
    url = f"{BASE_URL}/login"
    data = {"email": "john@example.com"}
    
    print_request("POST", url, data)
    
    response = requests.post(url, json=data)
    print_response(response)
    
    if response.status_code == 200:
        token = response.json()['data']['token']
        print(f"\n💾 User Token Saved for subsequent requests")
        return token
    return None

def test_4_get_all_users():
    """Test 4: Get All Users - Retrieve all users (no auth required)"""
    print_header("TEST 4: Get All Users")
    
    url = f"{BASE_URL}/users"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 200

def test_5_get_users_by_role():
    """Test 5: Get Users Filtered by Role"""
    print_header("TEST 5: Get Users Filtered by Role (Admin)")
    
    url = f"{BASE_URL}/users?role=admin"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 200

def test_6_get_user_by_id():
    """Test 6: Get User by ID - Retrieve specific user"""
    print_header("TEST 6: Get User by ID")
    
    url = f"{BASE_URL}/users/1"
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 200

def test_7_create_user_valid(admin_token):
    """Test 7: Create User with Valid Data"""
    print_header("TEST 7: Create User - Valid Data")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 28,
        "role": "user"
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("POST", url, data, headers)
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    
    if response.status_code == 201:
        user_id = response.json()['data']['id']
        print(f"\n✅ User created with ID: {user_id}")
        return user_id
    return None

def test_8_create_user_without_token():
    """Test 8: Create User Without Token - Should Fail (401)"""
    print_header("TEST 8: Create User - Without Token (Expect 401)")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "age": 30
    }
    
    print_request("POST", url, data)
    print("   ⚠️  No Authorization header")
    
    response = requests.post(url, json=data)
    print_response(response)
    
    return response.status_code == 401

def test_9_create_user_missing_field(admin_token):
    """Test 9: Create User - Missing Required Field (Expect 400)"""
    print_header("TEST 9: Create User - Missing Email (Expect 400)")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "Charlie Brown",
        "age": 25
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("POST", url, data, headers)
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    
    return response.status_code == 400

def test_10_create_user_invalid_email(admin_token):
    """Test 10: Create User - Invalid Email Format (Expect 400)"""
    print_header("TEST 10: Create User - Invalid Email (Expect 400)")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "David Lee",
        "email": "not-an-email",
        "age": 27
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("POST", url, data, headers)
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    
    return response.status_code == 400

def test_11_create_user_short_name(admin_token):
    """Test 11: Create User - Name Too Short (Expect 400)"""
    print_header("TEST 11: Create User - Short Name (Expect 400)")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "Ed",  # Only 2 characters
        "email": "ed@example.com",
        "age": 25
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("POST", url, data, headers)
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    
    return response.status_code == 400

def test_12_create_user_under_age(admin_token):
    """Test 12: Create User - Age Under 18 (Expect 400)"""
    print_header("TEST 12: Create User - Underage (Expect 400)")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "Young Person",
        "email": "young@example.com",
        "age": 17
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("POST", url, data, headers)
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    
    return response.status_code == 400

def test_13_create_user_duplicate_email(admin_token):
    """Test 13: Create User - Duplicate Email (Expect 409)"""
    print_header("TEST 13: Create User - Duplicate Email (Expect 409)")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "Another Admin",
        "email": "admin@example.com",  # Already exists
        "age": 30
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("POST", url, data, headers)
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    
    return response.status_code == 409

def test_14_create_user_boundary_age_18(admin_token):
    """Test 14: Create User - Boundary Test (Age = 18)"""
    print_header("TEST 14: Create User - Boundary Age 18 (Should Pass)")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "Exactly Eighteen",
        "email": "eighteen@example.com",
        "age": 18
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("POST", url, data, headers)
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    
    if response.status_code == 201:
        user_id = response.json()['data']['id']
        return user_id
    return None

def test_15_create_user_boundary_name_3(admin_token):
    """Test 15: Create User - Boundary Test (Name = 3 chars)"""
    print_header("TEST 15: Create User - Boundary Name 3 Chars (Should Pass)")
    
    url = f"{BASE_URL}/users"
    data = {
        "name": "Tim",  # Exactly 3 characters
        "email": "tim@example.com",
        "age": 25
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("POST", url, data, headers)
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    
    if response.status_code == 201:
        user_id = response.json()['data']['id']
        return user_id
    return None

def test_16_update_user(admin_token, user_id):
    """Test 16: Update User - Valid Data"""
    print_header("TEST 16: Update User - Valid Data")
    
    url = f"{BASE_URL}/users/{user_id}"
    data = {
        "name": "Alice Johnson Updated",
        "age": 29
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("PUT", url, data, headers)
    
    response = requests.put(url, json=data, headers=headers)
    print_response(response)
    
    return response.status_code == 200

def test_17_update_user_not_found(admin_token):
    """Test 17: Update Non-existent User (Expect 404)"""
    print_header("TEST 17: Update User - Not Found (Expect 404)")
    
    url = f"{BASE_URL}/users/999"
    data = {
        "name": "Updated Name"
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("PUT", url, data, headers)
    
    response = requests.put(url, json=data, headers=headers)
    print_response(response)
    
    return response.status_code == 404

def test_18_update_user_duplicate_email(admin_token, user_id):
    """Test 18: Update User - Duplicate Email (Expect 409)"""
    print_header("TEST 18: Update User - Duplicate Email (Expect 409)")
    
    url = f"{BASE_URL}/users/{user_id}"
    data = {
        "email": "admin@example.com"  # Already exists
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("PUT", url, data, headers)
    
    response = requests.put(url, json=data, headers=headers)
    print_response(response)
    
    return response.status_code == 409

def test_19_delete_user_as_regular_user(user_token, user_id):
    """Test 19: Delete User as Regular User - Should Fail (403)"""
    print_header("TEST 19: Delete User - As Regular User (Expect 403)")
    
    url = f"{BASE_URL}/users/{user_id}"
    headers = {"Authorization": f"Bearer {user_token}"}
    
    print_request("DELETE", url, headers=headers)
    print("   ⚠️  Using regular user token (not admin)")
    
    response = requests.delete(url, headers=headers)
    print_response(response)
    
    return response.status_code == 403

def test_20_delete_user_as_admin(admin_token, user_id):
    """Test 20: Delete User as Admin - Should Succeed"""
    print_header("TEST 20: Delete User - As Admin (Should Succeed)")
    
    url = f"{BASE_URL}/users/{user_id}"
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("DELETE", url, headers=headers)
    print("   ✅ Using admin token")
    
    response = requests.delete(url, headers=headers)
    print_response(response)
    
    return response.status_code == 200

def test_21_delete_user_not_found(admin_token):
    """Test 21: Delete Non-existent User (Expect 404)"""
    print_header("TEST 21: Delete User - Not Found (Expect 404)")
    
    url = f"{BASE_URL}/users/999"
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print_request("DELETE", url, headers=headers)
    
    response = requests.delete(url, headers=headers)
    print_response(response)
    
    return response.status_code == 404

def test_22_delete_user_without_token(user_id):
    """Test 22: Delete User Without Token (Expect 401)"""
    print_header("TEST 22: Delete User - Without Token (Expect 401)")
    
    url = f"{BASE_URL}/users/{user_id}"
    
    print_request("DELETE", url)
    print("   ⚠️  No Authorization header")
    
    response = requests.delete(url)
    print_response(response)
    
    return response.status_code == 401

def test_23_get_user_invalid_id():
    """Test 23: Get User with Invalid ID Format (Expect 400)"""
    print_header("TEST 23: Get User - Invalid ID Format (Expect 400)")
    
    url = f"{BASE_URL}/users/abc"
    
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 400

def test_24_get_user_not_found():
    """Test 24: Get Non-existent User (Expect 404)"""
    print_header("TEST 24: Get User - Not Found (Expect 404)")
    
    url = f"{BASE_URL}/users/999"
    
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 404

def test_25_login_invalid_email():
    """Test 25: Login with Invalid Email Format (Expect 400)"""
    print_header("TEST 25: Login - Invalid Email (Expect 400)")
    
    url = f"{BASE_URL}/login"
    data = {"email": "not-an-email"}
    
    print_request("POST", url, data)
    
    response = requests.post(url, json=data)
    print_response(response)
    
    return response.status_code == 400

def test_26_login_user_not_found():
    """Test 26: Login with Non-existent Email (Expect 404)"""
    print_header("TEST 26: Login - User Not Found (Expect 404)")
    
    url = f"{BASE_URL}/login"
    data = {"email": "notfound@example.com"}
    
    print_request("POST", url, data)
    
    response = requests.post(url, json=data)
    print_response(response)
    
    return response.status_code == 404

def test_27_simulate_error():
    """Test 27: Simulate Internal Server Error (Expect 500)"""
    print_header("TEST 27: Simulate Error - 500 Internal Server Error")
    
    url = f"{BASE_URL}/error"
    
    print_request("GET", url)
    
    response = requests.get(url)
    print_response(response)
    
    return response.status_code == 500

def test_28_reset_data():
    """Test 28: Reset Data Store to Initial State"""
    print_header("TEST 28: Reset Data Store")
    
    url = f"{BASE_URL}/reset"
    
    print_request("POST", url)
    
    response = requests.post(url)
    print_response(response)
    
    return response.status_code == 200

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all test scenarios"""
    
    print("\n" + "="*70)
    print("  API TESTING GUIDE - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\n📚 This script will test all API endpoints with various scenarios")
    print("   including positive cases, negative cases, and edge cases.\n")
    
    # Check if server is running
    if not wait_for_server():
        return
    
    # Track results
    results = []
    
    try:
        # Test 1: Health Check
        results.append(("Health Check", test_1_health_check()))
        sleep(0.5)
        
        # Test 2-3: Authentication
        admin_token = test_2_login_admin()
        sleep(0.5)
        user_token = test_3_login_regular_user()
        sleep(0.5)
        
        if not admin_token or not user_token:
            print("\n❌ Failed to get authentication tokens. Cannot continue.")
            return
        
        # Test 4-6: Read operations
        results.append(("Get All Users", test_4_get_all_users()))
        sleep(0.5)
        results.append(("Get Users by Role", test_5_get_users_by_role()))
        sleep(0.5)
        results.append(("Get User by ID", test_6_get_user_by_id()))
        sleep(0.5)
        
        # Test 7: Create valid user
        created_user_id = test_7_create_user_valid(admin_token)
        sleep(0.5)
        
        # Test 8-15: Create operations (negative & boundary tests)
        results.append(("Create Without Token", test_8_create_user_without_token()))
        sleep(0.5)
        results.append(("Create Missing Field", test_9_create_user_missing_field(admin_token)))
        sleep(0.5)
        results.append(("Create Invalid Email", test_10_create_user_invalid_email(admin_token)))
        sleep(0.5)
        results.append(("Create Short Name", test_11_create_user_short_name(admin_token)))
        sleep(0.5)
        results.append(("Create Underage", test_12_create_user_under_age(admin_token)))
        sleep(0.5)
        results.append(("Create Duplicate Email", test_13_create_user_duplicate_email(admin_token)))
        sleep(0.5)
        boundary_user_1 = test_14_create_user_boundary_age_18(admin_token)
        sleep(0.5)
        boundary_user_2 = test_15_create_user_boundary_name_3(admin_token)
        sleep(0.5)
        
        # Test 16-18: Update operations
        if created_user_id:
            results.append(("Update User", test_16_update_user(admin_token, created_user_id)))
            sleep(0.5)
        results.append(("Update Not Found", test_17_update_user_not_found(admin_token)))
        sleep(0.5)
        if created_user_id:
            results.append(("Update Duplicate Email", test_18_update_user_duplicate_email(admin_token, created_user_id)))
            sleep(0.5)
        
        # Test 19-22: Delete operations
        if created_user_id:
            results.append(("Delete as User (Forbidden)", test_19_delete_user_as_regular_user(user_token, created_user_id)))
            sleep(0.5)
            results.append(("Delete as Admin", test_20_delete_user_as_admin(admin_token, created_user_id)))
            sleep(0.5)
        results.append(("Delete Not Found", test_21_delete_user_not_found(admin_token)))
        sleep(0.5)
        if boundary_user_1:
            results.append(("Delete Without Token", test_22_delete_user_without_token(boundary_user_1)))
            sleep(0.5)
        
        # Test 23-26: Error scenarios
        results.append(("Get Invalid ID", test_23_get_user_invalid_id()))
        sleep(0.5)
        results.append(("Get Not Found", test_24_get_user_not_found()))
        sleep(0.5)
        results.append(("Login Invalid Email", test_25_login_invalid_email()))
        sleep(0.5)
        results.append(("Login Not Found", test_26_login_user_not_found()))
        sleep(0.5)
        
        # Test 27: Error simulation
        results.append(("Simulate Error", test_27_simulate_error()))
        sleep(0.5)
        
        # Test 28: Reset data
        results.append(("Reset Data", test_28_reset_data()))
        
        # Clean up remaining boundary users
        if boundary_user_1:
            requests.delete(f"{BASE_URL}/users/{boundary_user_1}", 
                          headers={"Authorization": f"Bearer {admin_token}"})
        if boundary_user_2:
            requests.delete(f"{BASE_URL}/users/{boundary_user_2}", 
                          headers={"Authorization": f"Bearer {admin_token}"})
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        return
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    print("\nDetailed Results:")
    
    for i, (name, result) in enumerate(results, 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {i:2d}. {status} - {name}")
    
    if passed == total:
        print(f"\n🎉 {Colors.GREEN}All tests passed successfully!{Colors.END}")
    else:
        print(f"\n⚠️  {Colors.YELLOW}{total - passed} test(s) failed{Colors.END}")
    
    print("\n" + "="*70)
    print("  Testing Complete!")
    print("="*70 + "\n")

# ============================================================================
# INDIVIDUAL TEST EXAMPLES
# ============================================================================

def example_create_user():
    """Example: How to create a user"""
    print("\n" + "="*70)
    print("EXAMPLE: Creating a User")
    print("="*70)
    
    # Step 1: Login to get token
    print("\nStep 1: Login to get authentication token")
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={"email": "admin@example.com"}
    )
    token = login_response.json()['data']['token']
    print(f"✅ Token obtained")
    
    # Step 2: Create user
    print("\nStep 2: Create user with valid data")
    user_data = {
        "name": "Example User",
        "email": "example@test.com",
        "age": 25,
        "role": "user"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    create_response = requests.post(
        f"{BASE_URL}/users",
        json=user_data,
        headers=headers
    )
    
    print(f"Status: {create_response.status_code}")
    print(f"Response: {json.dumps(create_response.json(), indent=2)}")

def example_update_user():
    """Example: How to update a user"""
    print("\n" + "="*70)
    print("EXAMPLE: Updating a User")
    print("="*70)
    
    # Step 1: Login
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={"email": "admin@example.com"}
    )
    token = login_response.json()['data']['token']
    
    # Step 2: Update user (assuming user ID 2 exists)
    user_id = 2
    update_data = {
        "name": "John Doe Updated",
        "age": 26
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    update_response = requests.put(
        f"{BASE_URL}/users/{user_id}",
        json=update_data,
        headers=headers
    )
    
    print(f"Status: {update_response.status_code}")
    print(f"Response: {json.dumps(update_response.json(), indent=2)}")

def example_delete_user():
    """Example: How to delete a user"""
    print("\n" + "="*70)
    print("EXAMPLE: Deleting a User (Admin Only)")
    print("="*70)
    
    # Step 1: Login as admin
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={"email": "admin@example.com"}
    )
    token = login_response.json()['data']['token']
    
    # Step 2: Create a user to delete
    user_data = {"name": "To Be Deleted", "email": "delete@test.com", "age": 25}
    create_response = requests.post(
        f"{BASE_URL}/users",
        json=user_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    user_id = create_response.json()['data']['id']
    
    # Step 3: Delete the user
    delete_response = requests.delete(
        f"{BASE_URL}/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status: {delete_response.status_code}")
    print(f"Response: {json.dumps(delete_response.json(), indent=2)}")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "example-create":
            example_create_user()
        elif command == "example-update":
            example_update_user()
        elif command == "example-delete":
            example_delete_user()
        else:
            print("Unknown command. Available commands:")
            print("  python api_testing_guide.py              - Run all tests")
            print("  python api_testing_guide.py example-create  - Show create example")
            print("  python api_testing_guide.py example-update  - Show update example")
            print("  python api_testing_guide.py example-delete  - Show delete example")
    else:
        # Run full test suite
        run_all_tests()
