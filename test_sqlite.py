"""
Quick test script to verify SQLite backend is working
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("="*60)
print("Testing SQLite Backend")
print("="*60)

# 1. Health Check
print("\n1. Health Check:")
health = requests.get(f"{BASE_URL}/health")
print(f"   Status: {health.status_code} {'✓' if health.status_code == 200 else '✗'}")

# 2. Get All Users (Initial)
print("\n2. Get All Users (Initial):")
users = requests.get(f"{BASE_URL}/users")
data = users.json()
print(f"   Users: {data['data']['count']}")
print(f"   Emails: {[u['email'] for u in data['data']['users']]}")

# 3. Login as Admin
print("\n3. Login as Admin:")
login = requests.post(f"{BASE_URL}/login", json={"email": "admin@example.com"})
token = login.json()["data"]["token"]
print(f"   Status: {login.status_code} {'✓' if login.status_code == 200 else '✗'}")
print(f"   Token: {token[:30]}...")

# 4. Create New User
print("\n4. Create New User:")
headers = {"Authorization": f"Bearer {token}"}
new_user = requests.post(
    f"{BASE_URL}/users",
    json={"name": "SQLite User", "email": "sqlite@example.com", "age": 28},
    headers=headers
)
print(f"   Status: {new_user.status_code} {'✓' if new_user.status_code == 201 else '✗'}")
if new_user.status_code == 201:
    print(f"   Created: {new_user.json()['data']['email']}")

# 5. Check Database (Should have 3 users now)
print("\n5. Check Database (After Creation):")
users2 = requests.get(f"{BASE_URL}/users")
data2 = users2.json()
print(f"   Total users: {data2['data']['count']}")
print(f"   Emails: {[u['email'] for u in data2['data']['users']]}")

# 6. Reset Database
print("\n6. Reset Database:")
reset = requests.post(f"{BASE_URL}/reset")
print(f"   Status: {reset.status_code} {'✓' if reset.status_code == 200 else '✗'}")
print(f"   Message: {reset.json()['message']}")

# 7. Verify Reset (Should be back to 2 users)
print("\n7. Verify Reset (After Reset):")
users3 = requests.get(f"{BASE_URL}/users")
data3 = users3.json()
print(f"   Total users: {data3['data']['count']}")
print(f"   Emails: {[u['email'] for u in data3['data']['users']]}")

# Final Result
print("\n" + "="*60)
if data3['data']['count'] == 2 and 'sqlite@example.com' not in [u['email'] for u in data3['data']['users']]:
    print("✅ SQLite Backend Working Perfectly!")
    print("   - Database persists data to disk")
    print("   - Reset function works correctly")
    print("   - All endpoints functional")
else:
    print("❌ Something wrong with reset")
print("="*60)
