# Manual API Testing Guide
## Complete Test Cases with Sample Data

This guide provides ready-to-use test cases for all API endpoints.
You can use these with Postman, cURL, or any HTTP client.

**Base URL**: `http://127.0.0.1:5000`

---

## 📋 Table of Contents
1. [Health & Utility Tests](#health--utility-tests)
2. [Authentication Tests](#authentication-tests)
3. [Create User Tests](#create-user-tests)
4. [Read User Tests](#read-user-tests)
5. [Update User Tests](#update-user-tests)
6. [Delete User Tests](#delete-user-tests)
7. [Error & Edge Cases](#error--edge-cases)

---

## Health & Utility Tests

### ✅ Test 1: Health Check
**Purpose**: Verify API is running

**Request**:
```
GET http://127.0.0.1:5000/health
```

**Expected Response** (200):
```json
{
  "status": "success",
  "data": {
    "status": "healthy",
    "timestamp": "2026-02-18T10:30:00.000000",
    "version": "1.0.0"
  },
  "message": "API is running successfully"
}
```

---

## Authentication Tests

### ✅ Test 2: Login as Admin
**Purpose**: Get JWT token for admin operations

**Request**:
```
POST http://127.0.0.1:5000/login
Content-Type: application/json

{
  "email": "admin@example.com"
}
```

**Expected Response** (200):
```json
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "name": "Admin User",
      "email": "admin@example.com",
      "role": "admin"
    }
  },
  "message": "Login successful"
}
```

**📝 Note**: Save the token from response for subsequent requests

---

### ✅ Test 3: Login as Regular User
**Request**:
```
POST http://127.0.0.1:5000/login
Content-Type: application/json

{
  "email": "john@example.com"
}
```

**Expected Response** (200): Similar to admin login

---

### ❌ Test 4: Login - Invalid Email Format
**Purpose**: Test email validation

**Request**:
```
POST http://127.0.0.1:5000/login
Content-Type: application/json

{
  "email": "not-an-email"
}
```

**Expected Response** (400):
```json
{
  "status": "error",
  "error_code": "INVALID_EMAIL",
  "message": "Invalid email format"
}
```

---

### ❌ Test 5: Login - User Not Found
**Request**:
```
POST http://127.0.0.1:5000/login
Content-Type: application/json

{
  "email": "notfound@example.com"
}
```

**Expected Response** (404):
```json
{
  "status": "error",
  "error_code": "USER_NOT_FOUND",
  "message": "User not found with provided email"
}
```

---

## Create User Tests

### ✅ Test 6: Create User - Valid Data
**Purpose**: Successfully create a new user

**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "age": 28,
  "role": "user"
}
```

**Expected Response** (201):
```json
{
  "status": "success",
  "data": {
    "id": 3,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "role": "user",
    "created_at": "2026-02-18T10:30:00.000000",
    "updated_at": "2026-02-18T10:30:00.000000"
  },
  "message": "User created successfully"
}
```

---

### ✅ Test 7: Create User - Without Role (Default to 'user')
**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Bob Smith",
  "email": "bob@example.com",
  "age": 30
}
```

**Expected**: User created with role="user" by default

---

### ❌ Test 8: Create User - Missing Required Field
**Purpose**: Test validation for missing email

**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Charlie Brown",
  "age": 25
}
```

**Expected Response** (400):
```json
{
  "status": "error",
  "error_code": "MISSING_FIELD",
  "message": "Missing required field: email"
}
```

---

### ❌ Test 9: Create User - Invalid Email
**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "David Lee",
  "email": "invalid-email",
  "age": 27
}
```

**Expected Response** (400):
```json
{
  "status": "error",
  "error_code": "INVALID_EMAIL",
  "message": "Invalid email format"
}
```

---

### ❌ Test 10: Create User - Name Too Short
**Purpose**: Test minimum name length (3 characters)

**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Ed",
  "email": "ed@example.com",
  "age": 25
}
```

**Expected Response** (400):
```json
{
  "status": "error",
  "error_code": "INVALID_NAME",
  "message": "Name must be at least 3 characters long"
}
```

---

### ❌ Test 11: Create User - Age Under 18
**Purpose**: Test minimum age requirement

**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Young Person",
  "email": "young@example.com",
  "age": 17
}
```

**Expected Response** (400):
```json
{
  "status": "error",
  "error_code": "INVALID_AGE",
  "message": "Age must be 18 or older"
}
```

---

### ❌ Test 12: Create User - Duplicate Email
**Purpose**: Test email uniqueness constraint

**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Another Admin",
  "email": "admin@example.com",
  "age": 30
}
```

**Expected Response** (409):
```json
{
  "status": "error",
  "error_code": "DUPLICATE_EMAIL",
  "message": "Email already exists. Please use a different email."
}
```

---

### ❌ Test 13: Create User - No Authorization Token
**Purpose**: Test authentication requirement

**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 25
}
```

**Expected Response** (401):
```json
{
  "status": "error",
  "error_code": "MISSING_TOKEN",
  "message": "Authorization token is missing. Please include a valid token in the request."
}
```

---

### ✅ Test 14: Create User - Boundary Test (Age = 18)
**Purpose**: Test exact boundary value

**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Exactly Eighteen",
  "email": "eighteen@example.com",
  "age": 18
}
```

**Expected**: Should succeed (201)

---

### ✅ Test 15: Create User - Boundary Test (Name = 3 chars)
**Request**:
```
POST http://127.0.0.1:5000/users
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Tim",
  "email": "tim@example.com",
  "age": 25
}
```

**Expected**: Should succeed (201)

---

## Read User Tests

### ✅ Test 16: Get All Users
**Purpose**: Retrieve list of all users (no auth required)

**Request**:
```
GET http://127.0.0.1:5000/users
```

**Expected Response** (200):
```json
{
  "status": "success",
  "data": {
    "users": [
      {
        "id": 1,
        "name": "Admin User",
        "email": "admin@example.com",
        "age": 30,
        "role": "admin",
        "created_at": "2026-02-18T10:00:00.000000",
        "updated_at": "2026-02-18T10:00:00.000000"
      },
      {
        "id": 2,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 25,
        "role": "user",
        "created_at": "2026-02-18T10:00:00.000000",
        "updated_at": "2026-02-18T10:00:00.000000"
      }
    ],
    "count": 2
  },
  "message": "Retrieved 2 user(s) successfully"
}
```

---

### ✅ Test 17: Get Users - Filter by Role
**Purpose**: Test query parameter filtering

**Request**:
```
GET http://127.0.0.1:5000/users?role=admin
```

**Expected**: Only admin users returned

---

### ✅ Test 18: Get User by ID
**Purpose**: Retrieve specific user

**Request**:
```
GET http://127.0.0.1:5000/users/1
```

**Expected Response** (200):
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Admin User",
    "email": "admin@example.com",
    "age": 30,
    "role": "admin",
    "created_at": "2026-02-18T10:00:00.000000",
    "updated_at": "2026-02-18T10:00:00.000000"
  },
  "message": "User retrieved successfully"
}
```

---

### ❌ Test 19: Get User - Invalid ID Format
**Purpose**: Test ID validation

**Request**:
```
GET http://127.0.0.1:5000/users/abc
```

**Expected Response** (400):
```json
{
  "status": "error",
  "error_code": "INVALID_USER_ID",
  "message": "User ID must be a valid integer"
}
```

---

### ❌ Test 20: Get User - Not Found
**Request**:
```
GET http://127.0.0.1:5000/users/999
```

**Expected Response** (404):
```json
{
  "status": "error",
  "error_code": "USER_NOT_FOUND",
  "message": "User with ID 999 not found"
}
```

---

## Update User Tests

### ✅ Test 21: Update User - Partial Update
**Purpose**: Update only specific fields

**Request**:
```
PUT http://127.0.0.1:5000/users/2
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "John Doe Updated",
  "age": 26
}
```

**Expected Response** (200):
```json
{
  "status": "success",
  "data": {
    "id": 2,
    "name": "John Doe Updated",
    "email": "john@example.com",
    "age": 26,
    "role": "user",
    "created_at": "2026-02-18T10:00:00.000000",
    "updated_at": "2026-02-18T11:00:00.000000"
  },
  "message": "User updated successfully"
}
```

---

### ✅ Test 22: Update User - Email Only
**Request**:
```
PUT http://127.0.0.1:5000/users/2
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "email": "john.updated@example.com"
}
```

**Expected**: Only email updated (200)

---

### ❌ Test 23: Update User - Not Found
**Request**:
```
PUT http://127.0.0.1:5000/users/999
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "name": "Updated Name"
}
```

**Expected Response** (404):
```json
{
  "status": "error",
  "error_code": "USER_NOT_FOUND",
  "message": "User with ID 999 not found"
}
```

---

### ❌ Test 24: Update User - Duplicate Email
**Purpose**: Test email uniqueness on update

**Request**:
```
PUT http://127.0.0.1:5000/users/2
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "email": "admin@example.com"
}
```

**Expected Response** (409):
```json
{
  "status": "error",
  "error_code": "DUPLICATE_EMAIL",
  "message": "Email already exists. Please use a different email."
}
```

---

### ❌ Test 25: Update User - Invalid Age
**Request**:
```
PUT http://127.0.0.1:5000/users/2
Content-Type: application/json
Authorization: Bearer {your_admin_token}

{
  "age": 15
}
```

**Expected Response** (400): Age validation error

---

## Delete User Tests

### ✅ Test 26: Delete User - As Admin
**Purpose**: Successfully delete user with admin token

**Request**:
```
DELETE http://127.0.0.1:5000/users/3
Authorization: Bearer {admin_token}
```

**Expected Response** (200):
```json
{
  "status": "success",
  "data": {
    "id": 3,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "role": "user",
    "created_at": "2026-02-18T10:30:00.000000",
    "updated_at": "2026-02-18T10:30:00.000000"
  },
  "message": "User deleted successfully"
}
```

---

### ❌ Test 27: Delete User - As Regular User (Forbidden)
**Purpose**: Test authorization requirement

**Request**:
```
DELETE http://127.0.0.1:5000/users/3
Authorization: Bearer {user_token}
```

**Expected Response** (403):
```json
{
  "status": "error",
  "error_code": "FORBIDDEN",
  "message": "Admin access required. You do not have permission to perform this action."
}
```

---

### ❌ Test 28: Delete User - Without Token
**Request**:
```
DELETE http://127.0.0.1:5000/users/3
```

**Expected Response** (401):
```json
{
  "status": "error",
  "error_code": "MISSING_TOKEN",
  "message": "Authorization token is missing. Please include a valid token in the request."
}
```

---

### ❌ Test 29: Delete User - Not Found
**Request**:
```
DELETE http://127.0.0.1:5000/users/999
Authorization: Bearer {admin_token}
```

**Expected Response** (404):
```json
{
  "status": "error",
  "error_code": "USER_NOT_FOUND",
  "message": "User with ID 999 not found"
}
```

---

## Error & Edge Cases

### ❌ Test 30: Method Not Allowed
**Purpose**: Test invalid HTTP method

**Request**:
```
PATCH http://127.0.0.1:5000/users/1
```

**Expected Response** (405):
```json
{
  "status": "error",
  "error_code": "METHOD_NOT_ALLOWED",
  "message": "Method PATCH not allowed for this endpoint"
}
```

---

### ❌ Test 31: Simulate Internal Server Error
**Purpose**: Test error handling

**Request**:
```
GET http://127.0.0.1:5000/error
```

**Expected Response** (500):
```json
{
  "status": "error",
  "error_code": "INTERNAL_SERVER_ERROR",
  "message": "Internal server error occurred"
}
```

---

### ✅ Test 32: Reset Data Store
**Purpose**: Reset to initial state (useful between test runs)

**Request**:
```
POST http://127.0.0.1:5000/reset
```

**Expected Response** (200):
```json
{
  "status": "success",
  "message": "Data store reset to initial state successfully"
}
```

---

## 🎯 Testing Workflow

### Recommended Order:

1. **Setup Phase**
   - Test 1: Health check
   - Test 2: Login as admin (save token)
   - Test 3: Login as user (save token)

2. **Read Operations**
   - Test 16: Get all users
   - Test 17: Filter by role
   - Test 18: Get user by ID

3. **Create Operations**
   - Test 6: Create valid user
   - Tests 8-13: Test all validation errors
   - Tests 14-15: Test boundary values

4. **Update Operations**
   - Test 21: Update user
   - Test 24: Try duplicate email

5. **Delete Operations**
   - Test 27: Try delete as regular user (should fail)
   - Test 26: Delete as admin (should succeed)

6. **Cleanup**
   - Test 32: Reset data

---

## 📝 Quick Test Data Sets

### Valid Users to Create:
```json
{
  "name": "Michael Scott",
  "email": "michael@dundermifflin.com",
  "age": 45,
  "role": "admin"
}

{
  "name": "Pam Beesly",
  "email": "pam@dundermifflin.com",
  "age": 28,
  "role": "user"
}

{
  "name": "Jim Halpert",
  "email": "jim@dundermifflin.com",
  "age": 30,
  "role": "user"
}

{
  "name": "Dwight Schrute",
  "email": "dwight@dundermifflin.com",
  "age": 35,
  "role": "user"
}
```

### Invalid Test Cases:
```json
// Missing email
{
  "name": "Invalid User",
  "age": 25
}

// Bad email format
{
  "name": "Bad Email",
  "email": "not-an-email",
  "age": 25
}

// Too young
{
  "name": "Too Young",
  "email": "young@example.com",
  "age": 16
}

// Name too short
{
  "name": "Al",
  "email": "al@example.com",
  "age": 25
}
```

---

## 🔧 cURL Examples

### Login:
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com"}'
```

### Create User:
```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"name": "Test User", "email": "test@example.com", "age": 25}'
```

### Get All Users:
```bash
curl http://127.0.0.1:5000/users
```

### Update User:
```bash
curl -X PUT http://127.0.0.1:5000/users/2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"name": "Updated Name", "age": 30}'
```

### Delete User:
```bash
curl -X DELETE http://127.0.0.1:5000/users/3 \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE"
```

---

## ✅ Test Checklist

Mark off as you complete each test:

- [ ] Health check works
- [ ] Can login as admin
- [ ] Can login as regular user
- [ ] Can get all users
- [ ] Can filter users by role
- [ ] Can get user by ID
- [ ] Can create user with valid data
- [ ] Missing field returns 400
- [ ] Invalid email returns 400
- [ ] Short name returns 400
- [ ] Underage returns 400
- [ ] Duplicate email returns 409
- [ ] No token returns 401
- [ ] Can update user
- [ ] Update validates duplicate email
- [ ] Regular user cannot delete (403)
- [ ] Admin can delete (200)
- [ ] Invalid ID returns 400
- [ ] Non-existent user returns 404
- [ ] Can reset data

---

## 📊 Expected Status Codes Summary

| Status | Meaning | When to Expect |
|--------|---------|----------------|
| 200 | OK | GET, PUT, DELETE success |
| 201 | Created | POST user success |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | Wrong HTTP method |
| 409 | Conflict | Duplicate email |
| 500 | Server Error | Internal error |

---

**End of Testing Guide**

For automated testing, use: `python api_testing_guide.py`
For Postman collection, import: `API_Backend_Postman_Collection.json`
