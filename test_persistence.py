"""
Test data persistence across server restarts
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

print("\n" + "="*60)
print("Testing Data Persistence Across Server Restarts")
print("="*60)

print("\nBefore you restart the server:")
print("1. Current users in database:")
users = requests.get(f"{BASE_URL}/users")
data = users.json()
print(f"   Total: {data['data']['count']}")
for user in data['data']['users']:
    print(f"   - {user['email']} (ID: {user['id']})")

print("\n" + "="*60)
print("Now RESTART the server (Ctrl+C and run 'python app.py' again)")
print("Then check if data persists!")
print("="*60)
print("\nWith SQLite: ✅ Data WILL persist (saved to users.db)")
print("With in-memory: ❌ Data would be lost")
print("="*60 + "\n")
