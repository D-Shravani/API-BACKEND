# API Backend - RESTful API for Testing & Automation Practice

A production-grade RESTful backend API built with Flask, designed specifically for teaching and practicing API testing and automation. This API includes realistic features, comprehensive validations, and various failure scenarios to provide a complete testing experience.

## 🎯 Purpose

This backend simulates a real enterprise API service with:
- Complete CRUD operations
- JWT authentication & authorization
- Comprehensive input validation
- Standardized response formats
- Multiple error scenarios
- Role-based access control

Perfect for QA engineers and automation testers to practice:
- API testing strategies
- Test automation frameworks
- Positive and negative test scenarios
- Authentication/Authorization testing
- Error handling validation

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd "API Backend"
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the server**
   ```bash
   python app.py
   ```

The API will be available at: `http://127.0.0.1:5000`

---

## 📋 API Endpoints

### Health Check

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/health` | No | Check API health status |

### Authentication

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/login` | No | Login and get JWT token |

### User Management

| Method | Endpoint | Auth Required | Admin Only | Description |
|--------|----------|---------------|------------|-------------|
| POST | `/users` | Yes | No | Create a new user |
| GET | `/users` | No | No | Get all users |
| GET | `/users/{id}` | No | No | Get user by ID |
| PUT | `/users/{id}` | Yes | No | Update user |
| DELETE | `/users/{id}` | Yes | **Yes** | Delete user |

### Utility Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/error` | No | Simulate 500 error for testing |
| POST | `/reset` | No | Reset data to initial state |

---

## 🔐 Authentication

### Login Flow

1. **Login to get JWT token**
   ```http
   POST /login
   Content-Type: application/json
   
   {
     "email": "admin@example.com"
   }
   ```

   **Response:**
   ```json
   {
     "status": "success",
     "data": {
       "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
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

2. **Use the token in subsequent requests**
   ```http
   GET /users
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
   ```

### Pre-seeded Users

The API comes with two pre-seeded users for testing:

1. **Admin User**
   - Email: `admin@example.com`
   - Role: `admin`
   - Can perform all operations including DELETE

2. **Regular User**
   - Email: `john@example.com`
   - Role: `user`
   - Cannot delete users

---

## 📝 API Documentation

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running

**Response:**
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

### 2. Login

**Endpoint:** `POST /login`

**Description:** Authenticate user and receive JWT token

**Request Body:**
```json
{
  "email": "admin@example.com"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
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

**Error Responses:**

**Missing Email (400):**
```json
{
  "status": "error",
  "error_code": "MISSING_FIELD",
  "message": "Missing required field: email"
}
```

**Invalid Email Format (400):**
```json
{
  "status": "error",
  "error_code": "INVALID_EMAIL",
  "message": "Invalid email format"
}
```

**User Not Found (404):**
```json
{
  "status": "error",
  "error_code": "USER_NOT_FOUND",
  "message": "User not found with provided email"
}
```

---

### 3. Create User

**Endpoint:** `POST /users`

**Authentication:** Required (JWT token)

**Request Body:**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "age": 28,
  "role": "user"
}
```

**Success Response (201):**
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

**Error Responses:**

**Missing Required Field (400):**
```json
{
  "status": "error",
  "error_code": "MISSING_FIELD",
  "message": "Missing required field: name"
}
```

**Name Too Short (400):**
```json
{
  "status": "error",
  "error_code": "INVALID_NAME",
  "message": "Name must be at least 3 characters long"
}
```

**Invalid Email (400):**
```json
{
  "status": "error",
  "error_code": "INVALID_EMAIL",
  "message": "Invalid email format"
}
```

**Age Less Than 18 (400):**
```json
{
  "status": "error",
  "error_code": "INVALID_AGE",
  "message": "Age must be 18 or older"
}
```

**Duplicate Email (409):**
```json
{
  "status": "error",
  "error_code": "DUPLICATE_EMAIL",
  "message": "Email already exists. Please use a different email."
}
```

**Unauthorized - No Token (401):**
```json
{
  "status": "error",
  "error_code": "MISSING_TOKEN",
  "message": "Authorization token is missing. Please include a valid token in the request."
}
```

---

### 4. Get All Users

**Endpoint:** `GET /users`

**Query Parameters:**
- `role` (optional): Filter by role (`admin` or `user`)

**Example:** `GET /users?role=admin`

**Success Response (200):**
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

### 5. Get User by ID

**Endpoint:** `GET /users/{id}`

**Example:** `GET /users/1`

**Success Response (200):**
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

**Error Responses:**

**Invalid User ID (400):**
```json
{
  "status": "error",
  "error_code": "INVALID_USER_ID",
  "message": "User ID must be a valid integer"
}
```

**User Not Found (404):**
```json
{
  "status": "error",
  "error_code": "USER_NOT_FOUND",
  "message": "User with ID 999 not found"
}
```

---

### 6. Update User

**Endpoint:** `PUT /users/{id}`

**Authentication:** Required (JWT token)

**Request Body (all fields optional):**
```json
{
  "name": "Jane Updated",
  "email": "jane.updated@example.com",
  "age": 30
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "id": 3,
    "name": "Jane Updated",
    "email": "jane.updated@example.com",
    "age": 30,
    "role": "user",
    "created_at": "2026-02-18T10:30:00.000000",
    "updated_at": "2026-02-18T11:00:00.000000"
  },
  "message": "User updated successfully"
}
```

**Error Responses:** Similar to Create User, plus User Not Found (404)

---

### 7. Delete User

**Endpoint:** `DELETE /users/{id}`

**Authentication:** Required (JWT token)

**Authorization:** Admin role required

**Success Response (200):**
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
  "message": "User deleted successfully"
}
```

**Error Responses:**

**Forbidden - Not Admin (403):**
```json
{
  "status": "error",
  "error_code": "FORBIDDEN",
  "message": "Admin access required. You do not have permission to perform this action."
}
```

**User Not Found (404):**
```json
{
  "status": "error",
  "error_code": "USER_NOT_FOUND",
  "message": "User with ID 999 not found"
}
```

---

## 🧪 Testing Scenarios

### Positive Test Cases

1. ✅ Successfully create a user with valid data
2. ✅ Retrieve all users
3. ✅ Retrieve a specific user by ID
4. ✅ Update user with valid data
5. ✅ Delete user as admin
6. ✅ Login with valid email
7. ✅ Access protected endpoint with valid token

### Negative Test Cases

1. ❌ Create user with missing required fields
2. ❌ Create user with invalid email format
3. ❌ Create user with duplicate email
4. ❌ Create user with age < 18
5. ❌ Create user with name < 3 characters
6. ❌ Get non-existent user (404)
7. ❌ Update non-existent user (404)
8. ❌ Delete user without token (401)
9. ❌ Delete user as non-admin (403)
10. ❌ Access protected endpoint with expired token
11. ❌ Access protected endpoint with invalid token
12. ❌ Invalid HTTP method (405)

### Boundary Test Cases

1. 🔍 Name with exactly 3 characters
2. 🔍 Age exactly 18
3. 🔍 Age = 150 (maximum)
4. 🔍 Age > 150 (should fail)
5. 🔍 Name with 100 characters

---

## 📊 Response Format

### Success Response Structure

```json
{
  "status": "success",
  "data": {...},
  "message": "Descriptive success message"
}
```

### Error Response Structure

```json
{
  "status": "error",
  "error_code": "ERROR_CODE",
  "message": "Human-readable error message"
}
```

### HTTP Status Codes Used

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 405 | Method Not Allowed | Invalid HTTP method |
| 409 | Conflict | Duplicate resource (email) |
| 500 | Internal Server Error | Server error |

---

## 🛠️ Project Structure

```
API Backend/
│
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models.py           # Data models and storage
├── validators.py       # Input validation logic
├── responses.py        # Response helper functions
├── auth.py             # Authentication & authorization
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

---

## 🔒 Security Features

- JWT token-based authentication
- Token expiration (1 hour)
- Role-based authorization
- Input validation and sanitization
- Email format validation
- SQL injection prevention (no SQL used)
- CORS enabled for cross-origin requests

---

## 🎓 For Test Automation Engineers

### Recommended Testing Tools

- **REST Clients:** Postman, Insomnia, Thunder Client
- **Automation Frameworks:** 
  - Python: pytest + requests
  - JavaScript: Jest + axios, Mocha + chai
  - Java: RestAssured + TestNG/JUnit
- **Performance Testing:** JMeter, Locust
- **API Documentation:** Swagger/OpenAPI (can be added)

### Testing Tips

1. **Start with Health Check** - Verify the API is running
2. **Test Authentication First** - Get valid tokens for protected endpoints
3. **Test CRUD in Order** - Create → Read → Update → Delete
4. **Reset Between Tests** - Use `/reset` endpoint to restore initial data
5. **Test Error Scenarios** - Don't just test happy paths
6. **Validate Response Schema** - Check all responses match expected format
7. **Check Status Codes** - Verify correct HTTP status for each scenario
8. **Test Authorization** - Verify admin vs user permissions

---

## 🐛 Troubleshooting

### Port Already in Use

If port 5000 is already in use, edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Token Expired

JWT tokens expire after 1 hour. Simply login again to get a new token.

### CORS Issues

CORS is enabled by default. If you encounter issues, verify `Flask-CORS` is installed.

---

## 📚 Additional Resources

### Postman Collection

Import this URL format to test APIs:
```
POST http://127.0.0.1:5000/login
GET http://127.0.0.1:5000/users
POST http://127.0.0.1:5000/users
```

### Sample Test Script (Python)

```python
import requests

# Base URL
BASE_URL = "http://127.0.0.1:5000"

# 1. Login
response = requests.post(f"{BASE_URL}/login", json={"email": "admin@example.com"})
token = response.json()["data"]["token"]

# 2. Create User
headers = {"Authorization": f"Bearer {token}"}
user_data = {
    "name": "Test User",
    "email": "test@example.com",
    "age": 25
}
response = requests.post(f"{BASE_URL}/users", json=user_data, headers=headers)
print(response.json())
```

---

## 📞 Support

This is an educational project for practicing API testing. Feel free to modify and extend it for your learning purposes.

---

## 📄 License

This project is open source and available for educational purposes.

---

## ✨ Version

**Current Version:** 1.0.0

**Last Updated:** February 18, 2026

---

**Happy Testing! 🚀**
