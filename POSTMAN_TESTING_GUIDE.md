# Postman API Testing Guide
## Complete Guide to Testing API Backend with Postman

This guide will walk you through testing all API endpoints using Postman.

---

## 📋 Table of Contents
1. [Setup Postman](#setup-postman)
2. [Import Collection](#import-collection)
3. [Setting Up Variables](#setting-up-variables)
4. [Authentication Flow](#authentication-flow)
5. [Testing All Endpoints](#testing-all-endpoints)
6. [Creating Test Scripts](#creating-test-scripts)
7. [Running Collections](#running-collections)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup Postman

### Step 1: Install Postman
1. Download Postman from: https://www.postman.com/downloads/
2. Install and launch Postman
3. Create a free account (optional but recommended)

### Step 2: Create a New Workspace
1. Click on "Workspaces" in the top menu
2. Click "Create Workspace"
3. Name it: "API Backend Testing"
4. Click "Create"

---

## 📥 Import Collection

### Option 1: Import the JSON File (Easiest)

1. Click the **"Import"** button (top left)
2. Select **"File"** tab
3. Click **"Upload Files"**
4. Navigate to: `C:\Users\Akram Alimaad\Desktop\API Backend`
5. Select: **`API_Backend_Postman_Collection.json`**
6. Click **"Import"**

✅ The collection "API Backend - Testing Collection" will appear in your Collections tab

### Option 2: Create Collection Manually

If you prefer to create it manually, follow the steps in the [Manual Collection Setup](#manual-collection-setup) section below.

---

## ⚙️ Setting Up Variables

### Environment Variables (Recommended)

1. Click the **"Environments"** icon (left sidebar, gear icon)
2. Click **"+ Create Environment"**
3. Name it: **"API Backend - Local"**
4. Add these variables:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://127.0.0.1:5000` | `http://127.0.0.1:5000` |
| `admin_token` | (leave empty) | (leave empty) |
| `user_token` | (leave empty) | (leave empty) |

5. Click **"Save"**
6. Select this environment from the dropdown (top right)

### Collection Variables (Already Set)

These are already set in the imported collection:
- `base_url`: `http://127.0.0.1:5000`
- `admin_token`: (empty, will be set automatically)
- `user_token`: (empty, will be set automatically)

---

## 🔐 Authentication Flow

### Step 1: Start the API Server

Before testing, ensure your API server is running:

```bash
cd "C:\Users\Akram Alimaad\Desktop\API Backend"
.\venv\Scripts\Activate.ps1
python app.py
```

You should see: `Running on http://127.0.0.1:5000`

### Step 2: Test Health Check

1. Open the **"Health Check"** request
2. Click **"Send"**
3. ✅ You should see **200 OK** response:
   ```json
   {
     "status": "success",
     "data": {
       "status": "healthy",
       "timestamp": "...",
       "version": "1.0.0"
     },
     "message": "API is running successfully"
   }
   ```

### Step 3: Login as Admin

1. Open the **"Login - Admin"** request
2. Review the request body:
   ```json
   {
     "email": "admin@example.com"
   }
   ```
3. Click **"Send"**
4. ✅ Response should be **200 OK** with a token
5. **Important**: The token is automatically saved to `{{admin_token}}`
6. You can verify in the **Tests** tab (scroll down):
   ```javascript
   if (pm.response.code === 200) {
       const response = pm.response.json();
       pm.collectionVariables.set('admin_token', response.data.token);
   }
   ```

### Step 4: Login as Regular User

1. Open the **"Login - Regular User"** request
2. Click **"Send"**
3. ✅ Token saved to `{{user_token}}`

---

## 🧪 Testing All Endpoints

### 1. Health & Utility Endpoints

#### ✅ Test: Health Check
**Request**: `GET {{base_url}}/health`

**Steps**:
1. Select "Health Check" request
2. Click "Send"
3. Verify: Status 200
4. Verify: Response contains `"status": "healthy"`

**Expected Response**:
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

### 2. Authentication Tests

#### ✅ Test: Login - Admin
**Request**: `POST {{base_url}}/login`

**Steps**:
1. Select "Login - Admin"
2. Go to **Body** tab → Raw → JSON
3. Verify body:
   ```json
   {
     "email": "admin@example.com"
   }
   ```
4. Click "Send"
5. Token is auto-saved to `{{admin_token}}`

**Expected**: Status 200, token received

#### ✅ Test: Login - Regular User
**Request**: `POST {{base_url}}/login`

**Body**:
```json
{
  "email": "john@example.com"
}
```

**Expected**: Status 200, token saved to `{{user_token}}`

---

### 3. Read Operations (No Auth Required)

#### ✅ Test: Get All Users
**Request**: `GET {{base_url}}/users`

**Steps**:
1. Select "Get All Users"
2. Click "Send"
3. No authentication needed

**Expected Response**:
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
        "created_at": "...",
        "updated_at": "..."
      },
      {
        "id": 2,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 25,
        "role": "user",
        "created_at": "...",
        "updated_at": "..."
      }
    ],
    "count": 2
  },
  "message": "Retrieved 2 user(s) successfully"
}
```

#### ✅ Test: Get Users - Filter by Role
**Request**: `GET {{base_url}}/users?role=admin`

**Steps**:
1. Select "Get Users - Filter by Role"
2. Check **Params** tab:
   - Key: `role`
   - Value: `admin`
3. Click "Send"

**Expected**: Only admin users returned

#### ✅ Test: Get User by ID
**Request**: `GET {{base_url}}/users/1`

**Expected**: Details of user with ID 1

---

### 4. Create Operations (Auth Required)

#### ✅ Test: Create User - Valid Data
**Request**: `POST {{base_url}}/users`

**Steps**:
1. Select "Create User - Valid"
2. Go to **Headers** tab
3. Verify Authorization header:
   - Key: `Authorization`
   - Value: `Bearer {{admin_token}}`
4. Go to **Body** tab
5. Update the JSON:
   ```json
   {
     "name": "Jane Smith",
     "email": "jane@example.com",
     "age": 28,
     "role": "user"
   }
   ```
6. Click "Send"

**Expected Response** (201 Created):
```json
{
  "status": "success",
  "data": {
    "id": 3,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 28,
    "role": "user",
    "created_at": "2026-02-18T10:30:00.000000",
    "updated_at": "2026-02-18T10:30:00.000000"
  },
  "message": "User created successfully"
}
```

💡 **Save the user ID** from response, you'll need it for update/delete tests!

---

### 5. Validation Tests (Should Fail)

#### ❌ Test: Create User - Missing Field
**Request**: `POST {{base_url}}/users`

**Body**:
```json
{
  "name": "Jane Smith",
  "age": 28
}
```
*Note: Email is missing*

**Expected Response** (400 Bad Request):
```json
{
  "status": "error",
  "error_code": "MISSING_FIELD",
  "message": "Missing required field: email"
}
```

#### ❌ Test: Create User - Invalid Email
**Body**:
```json
{
  "name": "Jane Smith",
  "email": "not-an-email",
  "age": 28
}
```

**Expected**: 400, `"error_code": "INVALID_EMAIL"`

#### ❌ Test: Create User - Short Name
**Body**:
```json
{
  "name": "Jo",
  "email": "jo@example.com",
  "age": 25
}
```

**Expected**: 400, `"error_code": "INVALID_NAME"`

#### ❌ Test: Create User - Under Age
**Body**:
```json
{
  "name": "Young User",
  "email": "young@example.com",
  "age": 17
}
```

**Expected**: 400, `"error_code": "INVALID_AGE"`

#### ❌ Test: Create User - Duplicate Email
**Body**:
```json
{
  "name": "Another Admin",
  "email": "admin@example.com",
  "age": 30
}
```

**Expected**: 409, `"error_code": "DUPLICATE_EMAIL"`

#### ❌ Test: Create User - No Token
**Steps**:
1. Select "Create User - No Token"
2. Go to **Headers** tab
3. Remove or disable the Authorization header
4. Click "Send"

**Expected**: 401, `"error_code": "MISSING_TOKEN"`

---

### 6. Update Operations

#### ✅ Test: Update User
**Request**: `PUT {{base_url}}/users/2`

**Steps**:
1. Select "Update User - Valid"
2. Ensure Authorization header has `{{admin_token}}`
3. Body (partial update):
   ```json
   {
     "name": "John Updated",
     "age": 26
   }
   ```
4. Click "Send"

**Expected Response** (200 OK):
```json
{
  "status": "success",
  "data": {
    "id": 2,
    "name": "John Updated",
    "email": "john@example.com",
    "age": 26,
    "role": "user",
    "created_at": "...",
    "updated_at": "2026-02-18T11:00:00.000000"
  },
  "message": "User updated successfully"
}
```

#### ❌ Test: Update User - Not Found
**Request**: `PUT {{base_url}}/users/999`

**Expected**: 404, `"error_code": "USER_NOT_FOUND"`

---

### 7. Delete Operations

#### ❌ Test: Delete as Regular User (Should Fail)
**Request**: `DELETE {{base_url}}/users/1`

**Steps**:
1. Select "Delete User - As Regular User"
2. Change Authorization to use `{{user_token}}`:
   - Value: `Bearer {{user_token}}`
3. Click "Send"

**Expected Response** (403 Forbidden):
```json
{
  "status": "error",
  "error_code": "FORBIDDEN",
  "message": "Admin access required. You do not have permission to perform this action."
}
```

#### ✅ Test: Delete as Admin (Should Succeed)
**Request**: `DELETE {{base_url}}/users/3`

**Steps**:
1. Select "Delete User - As Admin"
2. Ensure Authorization: `Bearer {{admin_token}}`
3. **Change the user ID** to the one you created earlier (e.g., 3)
4. Click "Send"

**Expected Response** (200 OK):
```json
{
  "status": "success",
  "data": {
    "id": 3,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 28,
    "role": "user",
    "created_at": "...",
    "updated_at": "..."
  },
  "message": "User deleted successfully"
}
```

#### ❌ Test: Delete User - Not Found
**Request**: `DELETE {{base_url}}/users/999`

**Expected**: 404, `"error_code": "USER_NOT_FOUND"`

---

### 8. Error & Utility Tests

#### ❌ Test: Simulate Error
**Request**: `GET {{base_url}}/error`

**Expected Response** (500 Internal Server Error):
```json
{
  "status": "error",
  "error_code": "INTERNAL_SERVER_ERROR",
  "message": "Internal server error occurred"
}
```

#### ✅ Test: Reset Data
**Request**: `POST {{base_url}}/reset`

**Purpose**: Reset database to initial state (useful between test runs)

**Expected Response** (200 OK):
```json
{
  "status": "success",
  "message": "Data store reset to initial state successfully"
}
```

---

## 📝 Creating Test Scripts in Postman

### Add Automatic Tests to Requests

You can add test scripts to automatically verify responses:

#### Example: Test for Login Request

1. Select "Login - Admin" request
2. Go to **Tests** tab
3. Add this script:

```javascript
// Test 1: Check status code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test 2: Check response structure
pm.test("Response has correct structure", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('status', 'success');
    pm.expect(jsonData).to.have.property('data');
    pm.expect(jsonData.data).to.have.property('token');
    pm.expect(jsonData.data).to.have.property('user');
});

// Test 3: Save token to variable
pm.test("Token is saved", function () {
    var jsonData = pm.response.json();
    pm.collectionVariables.set('admin_token', jsonData.data.token);
    pm.expect(jsonData.data.token).to.be.a('string');
});

// Test 4: Verify user role
pm.test("User is admin", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.data.user.role).to.eql('admin');
});
```

4. Click "Send"
5. Check **Test Results** tab to see all tests pass ✅

#### Example: Test for Create User Request

```javascript
// Verify status code
pm.test("Status code is 201 Created", function () {
    pm.response.to.have.status(201);
});

// Verify response structure
pm.test("User created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.status).to.eql('success');
    pm.expect(jsonData.data).to.have.property('id');
    pm.expect(jsonData.data).to.have.property('email');
});

// Verify data
pm.test("User has correct data", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.data.age).to.be.at.least(18);
    pm.expect(jsonData.data.name).to.be.a('string');
});

// Save user ID for later
pm.collectionVariables.set('created_user_id', pm.response.json().data.id);
```

#### Example: Test for Validation Errors

```javascript
// Verify error status code
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

// Verify error response
pm.test("Returns validation error", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.status).to.eql('error');
    pm.expect(jsonData).to.have.property('error_code');
    pm.expect(jsonData).to.have.property('message');
});
```

---

## 🏃 Running Collections (Automation)

### Run Entire Collection

1. Click on the collection name: "API Backend - Testing Collection"
2. Click the **"Run"** button (top right)
3. **Collection Runner** opens
4. Configure:
   - Select all requests or specific ones
   - Set **Delay** between requests: 500ms (recommended)
   - **Iterations**: 1
5. Click **"Run API Backend - Testing Collection"**
6. Watch tests execute automatically!
7. View **Test Results** summary

### Expected Results:
- All tests should pass ✅
- You'll see pass/fail for each request
- Total time taken
- Any errors highlighted in red

---

## 🔧 Advanced Postman Features

### Pre-request Scripts

Add logic before sending request:

```javascript
// Generate random email
pm.collectionVariables.set('random_email', 
    'user' + Math.floor(Math.random() * 10000) + '@example.com'
);

// Add timestamp
pm.collectionVariables.set('timestamp', new Date().toISOString());
```

### Console Debugging

View detailed logs:
1. Click **"Console"** (bottom left)
2. Shows all requests/responses
3. Useful for debugging

### Save Responses

1. After sending request
2. Click **"Save Response"**
3. Add to **Examples**
4. Document your API

---

## 📊 Organizing Tests

### Create Folders

Organize your requests:
1. Right-click collection
2. "Add Folder"
3. Create folders:
   - 📁 Authentication
   - 📁 User Management
   - 📁 Validation Tests
   - 📁 Error Scenarios

### Rename Requests

Make names descriptive:
- ❌ Bad: "Request 1"
- ✅ Good: "Create User - Valid Data (201)"

---

## ✅ Test Checklist

Complete this checklist in Postman:

### Setup
- [ ] Postman installed
- [ ] Collection imported
- [ ] Environment created
- [ ] Variables configured
- [ ] API server running

### Authentication
- [ ] Health check (200)
- [ ] Login as admin (200)
- [ ] Login as regular user (200)
- [ ] Token saved to variables

### Read Operations
- [ ] Get all users (200)
- [ ] Filter by role (200)
- [ ] Get user by ID (200)
- [ ] Get invalid ID (400)
- [ ] Get non-existent user (404)

### Create Operations
- [ ] Create valid user (201)
- [ ] Create without token (401)
- [ ] Create missing field (400)
- [ ] Create invalid email (400)
- [ ] Create short name (400)
- [ ] Create underage (400)
- [ ] Create duplicate email (409)

### Update Operations
- [ ] Update user (200)
- [ ] Update non-existent (404)
- [ ] Update duplicate email (409)

### Delete Operations
- [ ] Delete as regular user (403)
- [ ] Delete as admin (200)
- [ ] Delete non-existent (404)
- [ ] Delete without token (401)

### Utilities
- [ ] Simulate error (500)
- [ ] Reset data (200)

---

## 🐛 Troubleshooting

### Problem: "Could not get response"

**Solution**:
1. Verify API server is running: `python app.py`
2. Check URL is correct: `http://127.0.0.1:5000`
3. Try health check endpoint first

### Problem: "401 Unauthorized"

**Solution**:
1. Make sure you've logged in first
2. Check Authorization header includes token
3. Token format: `Bearer {{admin_token}}`
4. Verify token variable is saved

### Problem: "403 Forbidden"

**Solution**:
1. You're using regular user token instead of admin
2. Delete operations require admin role
3. Re-login as admin: `admin@example.com`

### Problem: Tests Failing

**Solution**:
1. Reset data: `POST {{base_url}}/reset`
2. Run requests in correct order
3. Check response body matches expected
4. Verify status codes

### Problem: Variables Not Saving

**Solution**:
1. Check Tests tab has the save script
2. Ensure environment is selected (top right)
3. Use collection variables instead

---

## 💡 Best Practices

### 1. Organize Your Workflow
- Start with authentication
- Test read operations first
- Then create, update, delete
- Reset data between test runs

### 2. Use Variables
- Don't hardcode URLs
- Use `{{base_url}}` everywhere
- Save tokens automatically

### 3. Add Tests
- Verify status codes
- Check response structure
- Validate data

### 4. Document As You Go
- Add descriptions to requests
- Save example responses
- Comment your test scripts

### 5. Reset Between Runs
- Use the `/reset` endpoint
- Keeps data consistent
- Prevents conflicts

---

## 📝 Quick Reference

### Common Status Codes
- 200: Success (GET, PUT, DELETE)
- 201: Created (POST)
- 400: Validation Error
- 401: Missing/Invalid Token
- 403: Forbidden (Not Admin)
- 404: Not Found
- 409: Conflict (Duplicate)
- 500: Server Error

### Pre-seeded Users
- Admin: `admin@example.com`
- User: `john@example.com`

### Required Headers
```
Content-Type: application/json
Authorization: Bearer {{token}}
```

---

## 🎓 Learning Path

### Beginner
1. Import collection
2. Run health check
3. Test login
4. Get all users
5. Create one user

### Intermediate
1. Add test scripts
2. Use variables
3. Test all CRUD operations
4. Handle errors properly

### Advanced
1. Run entire collection
2. Create custom tests
3. Use pre-request scripts
4. Export and share collection
5. Integrate with CI/CD

---

## 📤 Export Your Work

### Export Collection
1. Right-click collection
2. "Export"
3. Choose "Collection v2.1"
4. Save file

### Export Environment
1. Click Environments icon
2. Select your environment
3. Click "..." → Export
4. Save file

### Share with Team
- Send JSON files
- Or use Postman Workspace (Team feature)

---

## 🎉 Congratulations!

You now know how to:
- ✅ Import and organize Postman collections
- ✅ Test all API endpoints
- ✅ Write automatic tests
- ✅ Use variables and environments
- ✅ Run automated test suites
- ✅ Debug and troubleshoot issues

**Happy Testing! 🚀**

---

## 📚 Additional Resources

- Postman Documentation: https://learning.postman.com/
- API Documentation: See `README.md`
- Sample Requests: See `sample_requests_responses.json`
- Automated Tests: Run `python api_testing_guide.py`

---

**Version**: 1.0.0  
**Last Updated**: February 18, 2026  
**API Base URL**: http://127.0.0.1:5000
